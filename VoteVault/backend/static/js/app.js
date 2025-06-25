// Global variables
let elections = [];
let candidates = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('VoteVault app initialized');
    
    // Test if DOM elements exist
    const pollsGrid = document.getElementById('pollsGrid');
    console.log('Polls grid found:', !!pollsGrid);
    
    if (pollsGrid) {
        pollsGrid.innerHTML = '<div class="loading">Initializing...</div>';
    }
    
    loadElections();
    loadResults();
    
    // Refresh results every 30 seconds
    setInterval(loadResults, 30000);
});

// Format vote counts without trailing zeros
function formatVoteCount(votes) {
    if (votes >= 1000000) {
        return (votes / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    } else if (votes >= 1000) {
        return (votes / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    } else {
        return votes.toString();
    }
}

// Load available elections
async function loadElections() {
    try {
        console.log('Loading elections...');
        const response = await fetch('/api/elections');
        if (!response.ok) {
            throw new Error('Failed to fetch elections');
        }
        
        elections = await response.json();
        console.log('Elections loaded:', elections.length);
        displayElections();
        populateElectionSelect();
        
    } catch (error) {
        console.error('Error loading elections:', error);
        document.getElementById('pollsGrid').innerHTML = 
            '<div class="error">Error fetching polls: ' + error.message + '</div>';
    }
}

// Display elections in the polls grid as a graph
function displayElections() {
    const pollsGrid = document.getElementById('pollsGrid');
    
    if (elections.length === 0) {
        pollsGrid.innerHTML = '<div class="no-polls">No active polls available</div>';
        return;
    }
    
    // Create individual candidate graphs for each election
    const pollsHTML = `
        <div class="polls-graph">
            <div class="polls-header">
                <h3>Active Elections Overview</h3>
                <div class="polls-stats">
                    <span class="total-polls">${elections.length} Active Elections</span>
                </div>
            </div>
            <div class="elections-container">
                ${elections.map(election => `
                    <div class="election-card">
                        <div class="election-header">
                            <h4>${election.title}</h4>
                            <div class="countdown" id="countdown-${election.id}">
                                <span class="countdown-label">Election ends in:</span>
                                <span class="countdown-time" id="time-${election.id}">Loading...</span>
                            </div>
                        </div>
                        <div class="election-chart-container">
                            <canvas id="electionChart-${election.id}" width="400" height="200"></canvas>
                        </div>
                        <div class="election-info">
                            <p>${election.description}</p>
                            <div class="election-meta">
                                <span class="election-type">${election.election_type}</span>
                                <span class="election-status ${election.status}">${election.status}</span>
                            </div>
                            <div class="election-dates">
                                <span>Start: ${new Date(election.start_date).toLocaleDateString()}</span>
                                <span>End: ${new Date(election.end_date).toLocaleDateString()}</span>
                            </div>
                        </div>
                        <div class="election-action">
                            <button class="view-results-btn" onclick="viewResults(${election.id})">View Detailed Results</button>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    pollsGrid.innerHTML = pollsHTML;
    
    // Initialize countdowns and charts
    setTimeout(() => {
        initializeCountdowns();
        loadElectionCharts();
    }, 100);
}

// Initialize countdown timers for all elections
function initializeCountdowns() {
    elections.forEach(election => {
        const endDate = new Date(election.end_date);
        updateCountdown(election.id, endDate);
        
        // Update countdown every second
        setInterval(() => {
            updateCountdown(election.id, endDate);
        }, 1000);
    });
}

// Update countdown for a specific election
function updateCountdown(electionId, endDate) {
    const now = new Date();
    let timeLeft;
    
    // Handle both date-only and datetime formats
    if (typeof endDate === 'string') {
        // If it's just a date, assume end of day
        if (endDate.includes(' ')) {
            timeLeft = new Date(endDate) - now;
        } else {
            const endDateTime = new Date(endDate + ' 23:59:59');
            timeLeft = endDateTime - now;
        }
    } else {
        timeLeft = endDate - now;
    }
    
    if (timeLeft <= 0) {
        document.getElementById(`time-${electionId}`).textContent = 'Election Ended';
        document.getElementById(`time-${electionId}`).className = 'countdown-time ended';
        return;
    }
    
    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
    
    const timeString = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    document.getElementById(`time-${electionId}`).textContent = timeString;
    
    // Add urgency styling for elections ending soon
    if (days === 0 && hours < 24) {
        document.getElementById(`time-${electionId}`).className = 'countdown-time urgent';
    } else if (days === 0 && hours < 48) {
        document.getElementById(`time-${electionId}`).className = 'countdown-time warning';
    } else {
        document.getElementById(`time-${electionId}`).className = 'countdown-time';
    }
}

// Load individual candidate charts for each election
async function loadElectionCharts() {
    console.log('Loading election charts for', elections.length, 'elections');
    
    for (const election of elections) {
        try {
            console.log(`Loading results for election ${election.id}: ${election.title}`);
            const response = await fetch(`/api/results/${election.id}`);
            console.log(`Response status for election ${election.id}:`, response.status);
            
            if (response.ok) {
                const results = await response.json();
                console.log(`Results for election ${election.id}:`, results);
                console.log(`Found ${results.results.length} candidates with votes`);
                createElectionChart(election.id, results);
            } else {
                console.error(`Failed to load results for election ${election.id}:`, response.status);
            }
        } catch (error) {
            console.error(`Error loading results for election ${election.id}:`, error);
        }
    }
}

// Create individual candidate chart for an election
function createElectionChart(electionId, results) {
    console.log(`Creating chart for election ${electionId}`);
    const ctx = document.getElementById(`electionChart-${electionId}`);
    if (!ctx) {
        console.error(`Chart canvas not found for election ${electionId}`);
        return;
    }
    
    console.log(`Canvas found for election ${electionId}, results:`, results);
    
    const candidates = results.results.map(r => r.candidate_name);
    const votes = results.results.map(r => r.vote_count);
    const percentages = results.results.map(r => r.percentage);
    
    console.log(`Chart data for election ${electionId}:`, {
        candidates: candidates,
        votes: votes,
        percentages: percentages
    });
    
    // Generate colors for candidates
    const colors = [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(255, 159, 64, 0.8)'
    ];
    
    const borderColors = colors.map(color => color.replace('0.8', '1'));
    
    try {
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: candidates,
                datasets: [{
                    label: 'Votes',
                    data: votes,
                    backgroundColor: colors.slice(0, candidates.length),
                    borderColor: borderColors.slice(0, candidates.length),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const candidate = candidates[context.dataIndex];
                                const voteCount = formatVoteCount(votes[context.dataIndex]);
                                const percentage = percentages[context.dataIndex];
                                return `${candidate}: ${voteCount} votes (${percentage}%)`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatVoteCount(value);
                            }
                        }
                    }
                }
            }
        });
        console.log(`Chart created successfully for election ${electionId}`);
    } catch (error) {
        console.error(`Error creating chart for election ${electionId}:`, error);
    }
}

// Populate election select dropdown
function populateElectionSelect() {
    const electionSelect = document.getElementById('electionSelect');
    electionSelect.innerHTML = '<option value="">Choose an election...</option>';
    
    elections.forEach(election => {
        const option = document.createElement('option');
        option.value = election.id;
        option.textContent = election.title;
        electionSelect.appendChild(option);
    });
}

// Load candidates for selected election
async function loadCandidates() {
    const electionId = document.getElementById('electionSelect').value;
    const candidateSelect = document.getElementById('candidateSelect');
    
    if (!electionId) {
        candidateSelect.disabled = true;
        candidateSelect.innerHTML = '<option value="">Choose a candidate...</option>';
        return;
    }
    
    try {
        const response = await fetch(`/api/elections/${electionId}/candidates`);
        if (!response.ok) {
            throw new Error('Failed to fetch candidates');
        }
        
        const candidatesList = await response.json();
        candidates[electionId] = candidatesList;
        
        candidateSelect.disabled = false;
        candidateSelect.innerHTML = '<option value="">Choose a candidate...</option>';
        
        candidatesList.forEach(candidate => {
            const option = document.createElement('option');
            option.value = candidate.id;
            option.textContent = `${candidate.name} (${candidate.party})`;
            candidateSelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading candidates:', error);
        candidateSelect.innerHTML = '<option value="">Error loading candidates</option>';
    }
}

// Cast a vote
async function castVote() {
    const electionId = document.getElementById('electionSelect').value;
    const candidateId = document.getElementById('candidateSelect').value;
    const voterId = document.getElementById('voterId').value;
    const voteMessage = document.getElementById('voteMessage');
    
    if (!electionId || !candidateId || !voterId) {
        voteMessage.innerHTML = '<div class="error">Please fill in all fields</div>';
        return;
    }
    
    try {
        const response = await fetch('/api/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                election_id: parseInt(electionId),
                candidate_id: parseInt(candidateId),
                voter_id: voterId
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            voteMessage.innerHTML = '<div class="success">Vote cast successfully!</div>';
            // Refresh results after voting
            setTimeout(loadResults, 1000);
        } else {
            voteMessage.innerHTML = `<div class="error">Error: ${result.error}</div>`;
        }
        
    } catch (error) {
        console.error('Error casting vote:', error);
        voteMessage.innerHTML = '<div class="error">Failed to cast vote</div>';
    }
}

// Load and display election results
async function loadResults() {
    try {
        const resultsGrid = document.getElementById('resultsGrid');
        resultsGrid.innerHTML = '<div class="loading">Loading live results...</div>';
        
        const resultsPromises = elections.map(election => 
            fetch(`/api/results/${election.id}`).then(res => res.json())
        );
        
        const results = await Promise.all(resultsPromises);
        
        // Store results globally for chart updates
        window.electionResults = {};
        results.forEach(result => {
            if (!result.error) {
                window.electionResults[result.election_id] = result;
            }
        });
        
        displayResults(results);
        
        // Update the polls chart with real vote data
        setTimeout(() => {
            updatePollsChart();
        }, 200);
        
    } catch (error) {
        console.error('Error loading results:', error);
        document.getElementById('resultsGrid').innerHTML = 
            '<div class="error">Error loading results: ' + error.message + '</div>';
    }
}

// Display election results with charts
function displayResults(results) {
    const resultsGrid = document.getElementById('resultsGrid');
    
    const resultsHTML = results.map(result => {
        if (result.error) {
            return `<div class="result-card error">Error loading results for election ${result.election_id}</div>`;
        }
        
        const election = elections.find(e => e.id === result.election_id);
        const totalVotes = result.total_votes;
        
        // Format vote counts without trailing zeros
        const formattedResults = result.results.map(r => ({
            ...r,
            vote_count_formatted: formatVoteCount(r.vote_count),
            vote_count_full: r.vote_count.toLocaleString(),
            percentage: totalVotes > 0 ? ((r.vote_count / totalVotes) * 100).toFixed(1) : 0
        }));
        
        return `
            <div class="result-card">
                <h3>${election ? election.title : `Election ${result.election_id}`}</h3>
                <div class="result-stats">
                    <div class="total-votes">Total Votes: ${formatVoteCount(totalVotes)} (${totalVotes.toLocaleString()})</div>
                </div>
                <div class="chart-container">
                    <canvas id="chart-${result.election_id}" width="400" height="200"></canvas>
                </div>
                <div class="candidate-results">
                    ${formattedResults.map(candidate => `
                        <div class="candidate-result">
                            <div class="candidate-info">
                                <span class="candidate-name">${candidate.candidate_name}</span>
                                <span class="candidate-party">${candidate.party}</span>
                            </div>
                            <div class="vote-info">
                                <span class="vote-count">${candidate.vote_count_formatted} votes</span>
                                <span class="vote-percentage">${candidate.percentage}%</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');
    
    resultsGrid.innerHTML = resultsHTML;
    
    // Create charts after DOM is updated
    setTimeout(() => {
        results.forEach(result => {
            if (!result.error) {
                createChart(result);
            }
        });
    }, 100);
}

// Create Chart.js doughnut chart for election results
function createChart(result) {
    const ctx = document.getElementById(`chart-${result.election_id}`);
    if (!ctx) return;
    
    const data = result.results.map(r => r.vote_count);
    const labels = result.results.map(r => r.candidate_name);
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ];
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed.toLocaleString()} votes (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Create a chart showing individual candidates and their votes
function createPollsChart() {
    const ctx = document.getElementById('pollsChart');
    if (!ctx) return;
    
    // Get all candidates and their votes for the chart
    const chartData = [];
    const chartLabels = [];
    const chartColors = [];
    
    // Color palette for candidates
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF',
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
    ];
    
    // Process each election and its candidates
    elections.forEach((election, electionIndex) => {
        const candidates = window.candidates[election.id] || [];
        candidates.forEach((candidate, candidateIndex) => {
            // Get vote count for this candidate (we'll fetch this from results)
            const voteCount = 0; // Will be updated when results are loaded
            chartLabels.push(`${candidate.name} (${election.election_type})`);
            chartData.push(voteCount);
            chartColors.push(colors[(electionIndex * 4 + candidateIndex) % colors.length]);
        });
    });
    
    const pollData = {
        labels: chartLabels,
        datasets: [{
            label: 'Candidate Votes',
            data: chartData,
            backgroundColor: chartColors,
            borderColor: chartColors.map(color => color.replace('0.8', '1')),
            borderWidth: 2
        }]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: pollData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed.y.toLocaleString()} votes`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000) {
                                return (value / 1000000).toFixed(1) + 'M';
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'K';
                            }
                            return value;
                        }
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

// Update the polls chart with real vote data
function updatePollsChart() {
    const ctx = document.getElementById('pollsChart');
    if (!ctx) return;
    
    // Get the existing chart
    const chart = Chart.getChart(ctx);
    if (!chart) return;
    
    // Update chart data with real vote counts
    const chartData = [];
    const chartLabels = [];
    
    elections.forEach((election) => {
        const candidates = window.candidates[election.id] || [];
        candidates.forEach((candidate) => {
            // Find vote count for this candidate from results
            const electionResults = window.electionResults ? window.electionResults[election.id] : null;
            const candidateResult = electionResults ? 
                electionResults.results.find(r => r.candidate_name === candidate.name) : null;
            const voteCount = candidateResult ? candidateResult.vote_count : 0;
            
            chartLabels.push(`${candidate.name} (${election.election_type})`);
            chartData.push(voteCount);
        });
    });
    
    // Update chart data
    chart.data.labels = chartLabels;
    chart.data.datasets[0].data = chartData;
    chart.update();
}

// View results for a specific election
function viewResults(electionId) {
    // Scroll to results section
    document.querySelector('.results-container').scrollIntoView({ 
        behavior: 'smooth' 
    });
    
    // Highlight the specific election result
    setTimeout(() => {
        const resultCard = document.querySelector(`#chart-${electionId}`).closest('.result-card');
        resultCard.style.border = '2px solid #007bff';
        setTimeout(() => {
            resultCard.style.border = '';
        }, 2000);
    }, 500);
} 