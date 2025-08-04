// VRBLL chat API
import express from 'express';
const router = express.Router();
router.get('/messages', (req, res) => res.json([]));
router.post('/send', (req, res) => res.json({success:true}));
export default router;
