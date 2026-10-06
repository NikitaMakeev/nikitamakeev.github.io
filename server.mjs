import http from 'node:http';
import { readFile, mkdir, open } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const dataDirectory = resolve(process.env.DATA_DIR || join(root, 'private-data'));
const host = process.env.HOST || '127.0.0.1';
const port = Number(process.env.PORT || 3000);
const rateLimits = new Map();
const acceptedIds = new Set();
const windowMs = 10 * 60 * 1000;
const maximumBody = 24 * 1024;
let writeQueue = Promise.resolve();

function send(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(data));
}

function rateAllowed(ip) {
  const now = Date.now();
  for (const [key, value] of rateLimits) if (value.expires <= now) rateLimits.delete(key);
  const record = rateLimits.get(ip) || { count: 0, expires: now + windowMs };
  record.count++;
  rateLimits.set(ip, record);
  return record.count <= 10;
}

async function saveInquiry(entry) {
  const write = writeQueue.then(async () => {
    if (acceptedIds.has(entry.requestId)) return;
    await mkdir(dataDirectory, { recursive: true, mode: 0o700 });
    const file = await open(join(dataDirectory, 'inquiries.ndjson'), 'a', 0o600);
    try {
      await file.writeFile(JSON.stringify(entry) + '\n', 'utf8');
      await file.sync();
    } finally {
      await file.close();
    }
    acceptedIds.add(entry.requestId);
    if (acceptedIds.size > 10000) acceptedIds.delete(acceptedIds.values().next().value);
  });
  writeQueue = write.catch(() => {});
  await write;
}

const server = http.createServer(async (req, res) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('X-Frame-Options', 'DENY');
  req.setTimeout(15000);
  try {
    const path = new URL(req.url, 'http://localhost').pathname;
    if ((req.method === 'GET' || req.method === 'HEAD') && (path === '/' || path === '/index.html')) {
      const page = await readFile(join(root, 'index.html'));
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache' });
      res.end(req.method === 'HEAD' ? undefined : page);
      return;
    }
    if ((req.method === 'GET' || req.method === 'HEAD') && path === '/photos/portfolioFacePhoto.png') {
      const photo = await readFile(join(root, 'photos', 'portfolioFacePhoto.png'));
      res.writeHead(200, { 'Content-Type': 'image/png', 'Cache-Control': 'no-cache' });
      res.end(req.method === 'HEAD' ? undefined : photo);
      return;
    }
    if (req.method === 'GET' && path === '/api/contact-status') return send(res, 200, { enabled: true });
    // Never serve arbitrary files: enquiries and server code stay private.
    if (path !== '/api/inquiries') return send(res, 404, { error: 'Not found' });
    if (req.method !== 'POST') {
      res.setHeader('Allow', 'POST');
      return send(res, 405, { error: 'Method not allowed' });
    }
    if (req.headers.origin && new URL(req.headers.origin).host !== req.headers.host) {
      return send(res, 403, { error: 'Origin not allowed' });
    }
    if (!/^application\/json(?:;|$)/i.test(req.headers['content-type'] || '')) {
      return send(res, 415, { error: 'JSON required' });
    }
    if (!rateAllowed(req.socket.remoteAddress)) return send(res, 429, { error: 'Try again later' });
    let size = 0;
    const chunks = [];
    for await (const chunk of req) {
      size += chunk.length;
      if (size > maximumBody) return send(res, 413, { error: 'Request too large' });
      chunks.push(chunk);
    }
    let body;
    try { body = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
    catch { return send(res, 400, { error: 'Invalid JSON' }); }
    if (!body || typeof body !== 'object' || Array.isArray(body)) return send(res, 400, { error: 'Invalid request' });
    const { requestId, name, email, message, language, website } = body;
    if (typeof website !== 'string' || website.length) return send(res, 400, { error: 'Invalid request' });
    if (typeof requestId !== 'string' || !/^[a-f0-9-]{36}$/i.test(requestId) ||
        typeof name !== 'string' || name.length > 100 ||
        typeof email !== 'string' || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ||
        typeof message !== 'string' || message.trim().length < 10 || message.length > 4000 ||
        !['en', 'et', 'ru'].includes(language)) {
      return send(res, 400, { error: 'Invalid fields' });
    }
    await saveInquiry({ requestId, receivedAt: new Date().toISOString(), name: name.trim(), email: email.trim(), message: message.trim(), language });
    send(res, 201, { accepted: true });
  } catch {
    send(res, 503, { error: 'Could not save enquiry' });
  }
});
server.headersTimeout = 10000;
server.requestTimeout = 20000;
server.listen(port, host, () => console.log(`Portfolio: http://${host}:${port}\nEnquiries: ${join(dataDirectory, 'inquiries.ndjson')}`));
