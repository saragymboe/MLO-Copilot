import { Paper, Typography } from '@mui/material';

export function EmptyState({ title, message }: { title: string; message: string }) {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6">{title}</Typography>
      <Typography color="text.secondary">{message}</Typography>
    </Paper>
  );
}
