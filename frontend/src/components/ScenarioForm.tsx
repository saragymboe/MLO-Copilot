import { Box, Button, MenuItem, Stack, TextField, Typography } from '@mui/material';

export function ScenarioForm() {
  return (
    <Box component="form" sx={{ display: 'grid', gap: 2 }}>
      <Typography variant="h5">Borrower scenario</Typography>
      <TextField label="Borrower scenario" multiline minRows={3} />
      <TextField label="State" />
      <TextField label="Transaction" select defaultValue="purchase">
        <MenuItem value="purchase">Purchase</MenuItem>
        <MenuItem value="refinance">Refinance</MenuItem>
      </TextField>
      <Button variant="contained">Analyze</Button>
    </Box>
  );
}
