import { Typography, Stack, Divider } from '@mui/material';
import type { Product } from '../types';

export function ProductDetailSections({ product }: { product: Product }) {
  return (
    <Stack spacing={2}>
      <Typography variant="h5">Overview</Typography>
      <Typography>{product.whatItIs}</Typography>
      <Divider />
      <Typography variant="h6">Best for</Typography>
      <Typography>{product.bestFor}</Typography>
      <Divider />
      <Typography variant="h6">Guidelines</Typography>
      <Typography>{product.guidelines[0] || 'Verify current lender guidelines.'}</Typography>
    </Stack>
  );
}
