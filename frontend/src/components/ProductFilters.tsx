import { Box, MenuItem, TextField } from '@mui/material';

export function ProductFilters() {
  return (
    <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', mb: 3 }}>
      <TextField label="Search" size="small" />
      <TextField label="Category" size="small" select>
        <MenuItem value="Non-QM">Non-QM</MenuItem>
        <MenuItem value="Alternative">Alternative</MenuItem>
        <MenuItem value="Investment">Investment</MenuItem>
      </TextField>
      <TextField label="Lender" size="small" />
      <TextField label="Occupancy" size="small" />
    </Box>
  );
}
