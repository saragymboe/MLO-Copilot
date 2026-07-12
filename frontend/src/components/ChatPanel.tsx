import { Box, Paper, Stack, TextField, Typography } from '@mui/material';

export function ChatPanel() {
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6">Ask the product assistant</Typography>
      <Stack spacing={2} sx={{ mt: 2 }}>
        <Typography color="text.secondary">Ask a question about product fit, documentation, or borrower clues.</Typography>
        <TextField label="Question" multiline minRows={3} />
      </Stack>
    </Paper>
  );
}
