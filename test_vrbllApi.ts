import request from 'supertest';
import express from 'express';
import vrbllApi from './vrbllApi';
describe('VRBLL API', () => {
  const app = express();
  app.use(express.json());
  app.use(vrbllApi);
  it('returns messages', async () => {
    const res = await request(app).get('/messages');
    expect(Array.isArray(res.body)).toBe(true);
  });
});
