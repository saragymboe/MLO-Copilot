export interface Product {
  id: string;
  name: string;
  category: string;
  lendersVisible: string[];
  whatItIs: string;
  problemSolved: string;
  bestFor: string;
  notIdealFor: string;
  borrowerClues: string[];
  occupancy: string[];
  transactionTypes: string[];
  incomeTypes: string[];
  propertyTypes: string[];
  questions: string[];
  redFlags: string[];
  clientExplanation: string;
  pricing: string;
  guidelines: string[];
  sourceNotes: string[];
  lastReviewedAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuthUser {
  username: string;
  groups?: string[];
  email?: string;
}
