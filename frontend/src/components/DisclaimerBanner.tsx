import { Alert } from '@mui/material';

export function DisclaimerBanner() {
  return (
    <Alert severity="info" sx={{ mb: 3 }}>
      Preliminary educational guidance only. This is not a loan approval or commitment to lend. Verify current lender guidelines, overlays, pricing, state availability, property eligibility, and underwriting requirements.
    </Alert>
  );
}
