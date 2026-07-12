import { Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchProduct } from '../api/client';
import { LoadingState } from '../components/LoadingState';
import { ProductDetailSections } from '../components/ProductDetailSections';
import type { Product } from '../types';

export function ProductDetailPage() {
  const { productId } = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  useEffect(() => {
    if (productId) {
      fetchProduct(productId).then(setProduct);
    }
  }, [productId]);
  if (!product) return <LoadingState />;
  return (
    <div>
      <Typography variant="h4">{product.name}</Typography>
      <ProductDetailSections product={product} />
    </div>
  );
}
