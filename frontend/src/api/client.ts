import { Product } from '../types';

const baseUrl = import.meta.env.VITE_API_BASE_URL || '';

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init.headers || {}),
    },
  });
  if (!response.ok) {
    throw new Error('Request failed');
  }
  return response.json() as Promise<T>;
}

export async function fetchProducts(): Promise<Product[]> {
  const response = await request<{ data: { items: Product[] } }>('/products');
  return response.data.items;
}

export async function fetchProduct(productId: string): Promise<Product> {
  const response = await request<{ data: Product }>(`/products/${productId}`);
  return response.data;
}
