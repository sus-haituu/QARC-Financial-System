document.addEventListener("DOMContentLoaded", () => {
    // Shared state
    let chart = null;
    let lineSeries = null;
    let modelData = [];

    const btn = document.getElementById('deep-analysis-btn');
    const feedContainer = document.getElementById('feed-container');
    const lstmValueObj = document.getElementById('lstm-value');
    const pulseDot = document.querySelector('.pulse-dot');

    function addFeedEntry(text, title="SENTINEL", isAlert=false) {
        const entry = document.createElement('div');
        entry.className = isAlert ? 'feed-entry signal-alert' : 'feed-entry';
        
        let headerHtml = '';
        if (isAlert) {
            headerHtml = `<div class="signal-header"><i class="ph ph-sparkle"></i> ${title}</div>`;
        } else {
            const timeRaw = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            headerHtml = `<div class="entry-meta">${title} • ${timeRaw}</div>`;
        }
        
        entry.innerHTML = `
            ${headerHtml}
            <p>${text}</p>
        `;
        feedContainer.prepend(entry);
    }

    try {
        // 1. Initialize Lightweight Chart
        const chartContainer = document.getElementById('tvchart');
        if (typeof LightweightCharts === 'undefined') {
            throw new Error("LightweightCharts CDN script failed to load properly. Check network connection or AdBlocker.");
        }
        
        chart = LightweightCharts.createChart(chartContainer, {
            layout: {
                background: { type: 'solid', color: 'transparent' },
                textColor: '#8b949e',
            },
            grid: {
                vertLines: { color: 'rgba(255, 255, 255, 0.05)', style: 3 },
                horzLines: { color: 'rgba(255, 255, 255, 0.05)', style: 3 },
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
            },
            rightPriceScale: {
                borderColor: 'rgba(255, 255, 255, 0.1)',
            },
            timeScale: {
                borderColor: 'rgba(255, 255, 255, 0.1)',
                timeVisible: true,
            },
        });

        const candleSeries = chart.addCandlestickSeries({
            upColor: '#2e66ff',
            downColor: '#f84464',
            borderVisible: false,
            wickUpColor: '#2e66ff',
            wickDownColor: '#f84464',
        });

        // Generate some mock BTC data for visualization context
        let time = Math.floor(Date.now() / 1000) - 86400 * 60;
        let price = 61000;
        for (let i = 0; i < 60; i++) {
            const volatility = (Math.random() - 0.5) * 1500;
            const open = price;
            const close = price + volatility;
            const high = Math.max(open, close) + Math.random() * 500;
            const low = Math.min(open, close) - Math.random() * 500;
            modelData.push({ time: time + i * 86400, open, high, low, close });
            price = close;
        }
        candleSeries.setData(modelData);
        
        // Line series for the prediction
        lineSeries = chart.addLineSeries({
            color: '#2e66ff',
            lineWidth: 2,
            lineStyle: 1, // Dotted
            crosshairMarkerVisible: true,
            lastValueVisible: true,
            priceLineVisible: true,
        });

        chart.timeScale().fitContent();
        
        // Handle Window Resize properly
        new ResizeObserver(entries => {
            if (entries.length === 0 || entries[0].target !== chartContainer || !chart) { return; }
            const newRect = entries[0].contentRect;
            chart.applyOptions({ height: newRect.height, width: newRect.width });
        }).observe(chartContainer);

    } catch (e) {
        console.error("Chart initialization failed:", e);
        addFeedEntry("Warning: Interactive Chart Modules failed to load (CDN Error). Data stream will still proceed securely.", "SYSTEM WARNING", true);
    }

    // 2. Fetch API Integration
    btn.addEventListener('click', async () => {
        // Prepare loading UI state
        btn.classList.add('loading');
        btn.querySelector('.btn-title').innerText = "PROCESSING KNOWLEDGE GRAPH...";
        pulseDot.style.backgroundColor = "#2e66ff";
        pulseDot.style.boxShadow = "0 0 10px #2e66ff";
        
        try {
            const res = await fetch("http://127.0.0.1:5000/api/analyze");
            const payload = await res.json();
            
            if (payload.status === "success") {
                const results = payload.data;
                const prediction = results.lstm_prediction;
                
                // Format price for LSTM UI Card
                const formattedPrice = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(prediction);
                lstmValueObj.innerText = formattedPrice;
                
                // Add the feed entry from AI
                addFeedEntry(results.llama_strategy, "QARC NEURAL CORE", true);
                
                // Draw dotted glowing line on chart to the prediction price IF chart loaded
                if (chart && lineSeries && modelData.length > 0) {
                    const lastCandle = modelData[modelData.length - 1];
                    const predictionTime = lastCandle.time + 86400 * 5; // projected 5 days out
                    lineSeries.setData([
                        { time: lastCandle.time, value: lastCandle.close },
                        { time: predictionTime, value: prediction }
                    ]);
                    
                    lineSeries.setMarkers([
                        { time: predictionTime, position: 'aboveBar', color: '#2e66ff', shape: 'circle', text: 'TARGET P/L' }
                    ]);
                    chart.timeScale().fitContent();
                }
            } else {
                addFeedEntry("Backend error: " + payload.message);
            }
        } catch (error) {
            addFeedEntry("Failed to connect to API Gateway. Ensure Flask is running on port 5000.");
            console.error(error);
        } finally {
            // Restore btn
            btn.classList.remove('loading');
            btn.querySelector('.btn-title').innerText = "EXECUTE DEEP ANALYSIS";
            pulseDot.style.backgroundColor = "var(--text-muted)";
            pulseDot.style.boxShadow = "none";
        }
    });
});
