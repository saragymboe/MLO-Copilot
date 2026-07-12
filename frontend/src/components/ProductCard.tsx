import { Card, CardContent, CardActions, Chip, Stack, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import type { Product } from '../types';

export function ProductCard({ product }: { product: Product }) {
  return (
    <Card>
      <CardContent>
        <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
          <Chip label={product.category} size="small" />
          <Chip label={product.lendersVisible[0] || 'Multiple'} size="small" variant="outlined" />
        </Stack>
        <Typography variant="h6">{product.name}</Typography>
        <Typography variant="body2" color="text.secondary">{product.problemSolved}</Typography>
      </CardContent>
      <CardActions>
        <Button component={Link} to={`/products/${product.id}`}>View details</Button>
      </CardActions>
    </Card>
  );
}
