import { Paper } from '@mui/material';
import { DisclaimerBanner } from '../components/DisclaimerBanner';
import { ScenarioForm } from '../components/ScenarioForm';
import { RecommendationCard } from '../components/RecommendationCard';

export function ScenarioFinderPage() {
  return (
    <div>
      <DisclaimerBanner />
      <Paper sx={{ p: 3 }}>
        <ScenarioForm />
      </Paper>
      <div style={{ marginTop: 16 }}>
        <RecommendationCard title="Bank Statement Loan" score={82} />
      </div>
    </div>
  );
}
