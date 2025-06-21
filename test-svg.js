import { renderStatsCard } from './src/cards/stats-card.js';

const stats = {
  name: 'testuser',
  totalStars: 100,
  totalCommits: 200,
  totalIssues: 50,
  totalPRs: 75,
  totalPRsMerged: 60,
  mergedPRsPercentage: 80,
  totalReviews: 30,
  totalDiscussionsStarted: 10,
  totalDiscussionsAnswered: 20,
  contributedTo: 5,
  rank: { level: 'A+', percentile: 1 }
};

const svg = renderStatsCard(stats, {theme: 'default', show_icons: true});
console.log(svg);
