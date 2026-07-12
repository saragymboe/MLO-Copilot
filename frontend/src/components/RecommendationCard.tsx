import { Card, CardContent, Typography, Stack, Chip } from '@mui/material';

export function RecommendationCard({ title, score }: { title: string; score: number }) {
  return (
    <Card>
      <CardContent>
        <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
          <Chip label={`${score}/100`} />
          <Chip label="Preliminary" variant="outlined" />
        </Stack>
        <Typography variant="h6">{title}</Typography>
        <Typography variant="body2">This recommendation should be validated against current lender guidelines and overlays.</Typography>
      </CardContent>
    </Card>
  );
}
