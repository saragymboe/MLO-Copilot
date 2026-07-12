import { Grid, Paper, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { DisclaimerBanner } from "../components/DisclaimerBanner";

const cards = [
  { title: "Search Products", path: "/products" },
  { title: "Analyze Borrower Scenario", path: "/scenarios" },
  { title: "Ask Product Assistant", path: "/chat" },
];

export function DashboardPage() {
  return (
    <div>
      <DisclaimerBanner />
      <Grid container spacing={2}>
        {cards.map((card) => (
          <Grid item xs={12} md={4} key={card.title}>
            <Paper sx={{ p: 3 }} component={Link} to={card.path}>
              <Typography variant="h6">{card.title}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}
