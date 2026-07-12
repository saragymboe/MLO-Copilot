import { Paper, Typography } from '@mui/material';

export function AdminProductsPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5">Admin Product Editor</Typography>
      <Typography color="text.secondary">Create, edit, archive, and import products here.</Typography>
    </Paper>
  );
}
