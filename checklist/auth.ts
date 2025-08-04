// JWT Auth and role-based authorization for checklist API
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

const JWT_SECRET = process.env.JWT_SECRET || 'akira-dev-secret';

export type UserRole = 'member' | 'reviewer';

export interface AuthUser {
  username: string;
  role: UserRole;
}

export function generateToken(user: AuthUser) {
  return jwt.sign(user, JWT_SECRET, { expiresIn: '12h' });
}

export function authenticateJWT(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader) return res.status(401).json({ error: 'No token' });
  const token = authHeader.split(' ')[1];
  try {
    const user = jwt.verify(token, JWT_SECRET) as AuthUser;
    (req as any).user = user;
    next();
  } catch {
    res.status(403).json({ error: 'Invalid token' });
  }
}

export function requireRole(role: UserRole) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = (req as any).user as AuthUser;
    if (!user || user.role !== role) {
      return res.status(403).json({ error: 'Insufficient role' });
    }
    next();
  };
}
