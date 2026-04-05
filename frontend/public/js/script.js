// Smooth scrolling and animations for SpaceX-inspired satellite property prediction website

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }

    // Smooth scroll to sections
    function scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const offsetTop = section.offsetTop - 70; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }

    // Make scrollToSection globally available
    window.scrollToSection = scrollToSection;

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(0, 0, 0, 0.95)';
                navbar.style.backdropFilter = 'blur(15px)';
            } else {
                navbar.style.background = 'rgba(0, 0, 0, 0.9)';
                navbar.style.backdropFilter = 'blur(10px)';
            }
        });
    }

    // Active navigation link highlighting
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    function highlightNavLink() {
        let current = '';
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = sectionId;
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', highlightNavLink);

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Add animation classes to elements
    const animatedElements = document.querySelectorAll('.step, .tech-card, .team-member, .about-text, .about-visual');
    animatedElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // Add staggered animations
    const staggeredElements = document.querySelectorAll('.tech-grid .tech-card, .team-grid .team-member');
    staggeredElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });

    // Add micro-interactions
    const interactiveElements = document.querySelectorAll('.cta-button, .demo-button, .tech-card, .team-member, .step');
    interactiveElements.forEach(el => {
        el.classList.add('interactive-element');
    });

    // Add glow effects to specific elements
    const glowElements = document.querySelectorAll('.cta-button.primary');
    glowElements.forEach(el => {
        el.classList.add('glow-effect');
    });

    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    const earth = document.querySelector('.earth');
    const stars = document.querySelector('.stars');

    if (hero && earth && stars) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallaxSpeed = 0.5;
            
            if (scrolled < window.innerHeight) {
                earth.style.transform = `translateY(-50%) translateX(${scrolled * parallaxSpeed}px)`;
                stars.style.transform = `translateY(${scrolled * parallaxSpeed * 0.3}px)`;
            }
        });
    }

    // Tech card hover effects
    const techCards = document.querySelectorAll('.tech-card');
    techCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Step cards hover effects
    const stepCards = document.querySelectorAll('.step');
    stepCards.forEach(step => {
        step.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        step.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Team member hover effects
    const teamMembers = document.querySelectorAll('.team-member');
    teamMembers.forEach(member => {
        member.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        member.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Button hover effects
    const buttons = document.querySelectorAll('.cta-button, .demo-button, .submit-button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const arrow = this.querySelector('.button-arrow');
            if (arrow) {
                arrow.style.transform = 'translateX(5px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            const arrow = this.querySelector('.button-arrow');
            if (arrow) {
                arrow.style.transform = 'translateX(0)';
            }
        });
    });

    // Form submission handling (demo purposes)
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const name = formData.get('name');
            const email = formData.get('email');
            const message = formData.get('message');
            
            if (!name || !email || !message) {
                alert('Please fill in all fields.');
                return;
            }
            
            const submitButton = this.querySelector('.submit-button');
            const originalText = submitButton.innerHTML;
            
            submitButton.innerHTML = '<span>Sending...</span>';
            submitButton.disabled = true;
            
            setTimeout(() => {
                alert('Thank you for your message! We\'ll get back to you soon.');
                this.reset();
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 2000);
        });
    }

    // Demo button functionality
    const demoButton = document.querySelector('.demo-button');
    if (demoButton) {
        demoButton.addEventListener('click', function() {
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            
            modal.innerHTML = `
                <div style="
                    background: #1a1a1a;
                    border: 1px solid #333;
                    border-radius: 10px;
                    padding: 40px;
                    max-width: 600px;
                    width: 90%;
                    text-align: center;
                    position: relative;
                    transform: scale(0.8);
                    transition: transform 0.3s ease;
                ">
                    <button onclick="this.parentElement.parentElement.remove()" style="
                        position: absolute;
                        top: 15px;
                        right: 15px;
                        background: none;
                        border: none;
                        color: #fff;
                        font-size: 24px;
                        cursor: pointer;
                    ">×</button>
                    <h3 style="color: #00d4ff; margin-bottom: 20px; font-size: 1.5rem;">Demo Concept</h3>
                    <p style="color: #ccc; margin-bottom: 20px; line-height: 1.6;">
                        Our satellite-based property prediction system analyzes high-resolution imagery to identify key factors that influence property values, including:
                    </p>
                    <ul style="color: #ccc; text-align: left; margin-bottom: 30px;">
                        <li>Neighborhood development patterns</li>
                        <li>Infrastructure proximity and quality</li>
                        <li>Environmental factors and green spaces</li>
                        <li>Urban growth indicators</li>
                        <li>Transportation accessibility</li>
                    </ul>
                    <p style="color: #ccc; font-size: 0.9rem;">
                        The AI model processes this data to generate accurate price predictions with confidence intervals.
                    </p>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            setTimeout(() => {
                modal.style.opacity = '1';
                modal.querySelector('div').style.transform = 'scale(1)';
            }, 10);
            
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        });
    }

    // Add scroll-based animations for better visual appeal
    function addScrollAnimations() {
        const elements = document.querySelectorAll('.section-title, .about-description, .contact-subtitle');
        
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        });
        
        const titleObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });
        
        elements.forEach(element => {
            titleObserver.observe(element);
        });
    }

    addScrollAnimations();

    // Add subtle cursor trail effect
    let mouseX = 0, mouseY = 0;
    let trail = [];

    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        if (trail.length > 10) {
            trail.shift();
        }
        
        trail.push({ x: mouseX, y: mouseY });
        
        trail.forEach((point, index) => {
            const opacity = (index + 1) / trail.length * 0.3;
            const size = (index + 1) / trail.length * 3;
            
            let trailElement = document.getElementById(`trail-${index}`);
            if (!trailElement) {
                trailElement = document.createElement('div');
                trailElement.id = `trail-${index}`;
                trailElement.style.cssText = `
                    position: fixed;
                    width: ${size}px;
                    height: ${size}px;
                    background: #00d4ff;
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 9999;
                    opacity: ${opacity};
                    transition: all 0.1s ease;
                `;
                document.body.appendChild(trailElement);
            }
            
            trailElement.style.left = point.x - size/2 + 'px';
            trailElement.style.top = point.y - size/2 + 'px';
        });
    });

    // Performance optimization: throttle scroll events
    let ticking = false;
    
    function updateOnScroll() {
        highlightNavLink();
        ticking = false;
    }
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateOnScroll);
            ticking = true;
        }
    });

    // Demo functionality - Load properties and handle predictions
    loadProperties();
    setupPredictionButton();

    function loadProperties() {
        fetch('http://127.0.0.1:5000/properties')
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('property-select');
                if (select) {
                    select.innerHTML = '<option value="">Select a property to analyze...</option>';
                    data.forEach(property => {
                        const option = document.createElement('option');
                        option.value = property.id;
                        option.textContent = `${property.streetAddress} (${property.zipcode})`;
                        select.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error loading properties:', error);
                const select = document.getElementById('property-select');
                if (select) {
                    select.innerHTML = '<option value="">Error loading properties</option>';
                }
            });
    }

    function setupPredictionButton() {
        const predictButton = document.getElementById('predict-button');
        const predictionResult = document.getElementById('prediction-result');
        const select = document.getElementById('property-select');
    
        if (!predictButton || !predictionResult || !select) return;
    
        predictButton.addEventListener('click', function() {
            const selectedId = select.value;
    
            if (!selectedId) {
                alert('Please select a property first.');
                return;
            }
    
            predictionResult.style.display = 'block';
            predictionResult.innerHTML = '<div class="loading-message">Loading prediction...</div>';
            predictButton.disabled = true;
    
            fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    property_index: parseInt(selectedId)
            })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    predictionResult.innerHTML = `<div class="error-message">Error: ${data.error}</div>`;
                    return;
                }
    
                const predictedPrice = data.predicted_price ? 
                    parseFloat(data.predicted_price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : "N/A";
                const actualPrice = data.actual_price ? 
                    parseFloat(data.actual_price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : "Not available";
    
                let predictionHTML = `
                    <div class="prediction-content">
                        <h3>🛰️ Satellite Analysis Complete</h3>
                        <div class="price-comparison">
                            <div class="price-item">
                                <span class="price-label">💰 Predicted Price:</span>
                                <span class="price-value predicted">$${predictedPrice}</span>
                            </div>
                            <div class="price-item">
                                <span class="price-label">🏠 Actual Price:</span>
                                <span class="price-value actual">$${actualPrice}</span>
                            </div>
                        </div>
                `;

                if (data.satellite_image) {
                    predictionHTML += `
                        <div class="satellite-image-container" style="margin-top: 20px;">
                            <h4>🛰️ Analyzed Satellite Image</h4>
                            <img src="${data.satellite_image}" alt="Satellite view of property" 
                                 style="max-width: 100%; border-radius: 10px; border: 2px solid #00d4ff; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);">
                    `;
                    
                    if (data.image_metadata) {
                        predictionHTML += `
                            <div class="image-metadata" style="margin-top: 10px; padding: 10px; background: rgba(26, 26, 46, 0.6); border-radius: 8px; font-size: 0.9em;">
                                <p><strong>📍 Location:</strong> ${data.image_metadata.location || 'Unknown'}</p>
                                <p><strong>📅 Capture Date:</strong> ${data.image_metadata.capture_date || 'Unknown'}</p>
                                <p><strong>🔍 Resolution:</strong> ${data.image_metadata.resolution || 'Unknown'}</p>
                            </div>
                        `;
                    }
                    
                    predictionHTML += `</div>`;
                }

                predictionHTML += `</div>`;
                predictionResult.innerHTML = predictionHTML;
            })
            .catch(err => {
                console.error('Error making prediction:', err);
                predictionResult.innerHTML = '<div class="error-message">Error connecting to prediction service.</div>';
            })
            .finally(() => predictButton.disabled = false);
        });
    }
});

// Property explanation functionality
function loadProperties() {
    const select = document.getElementById('property-select');
    if (!select) return;

    fetch('http://localhost:5000/properties')
        .then(response => response.json())
        .then(data => {
            select.innerHTML = '<option value="">Select a property to explain...</option>';
            data.forEach(property => {
                const option = document.createElement('option');
                option.value = property.id;
                option.textContent = `${property.streetAddress} (${property.zipcode})`;
                select.appendChild(option);
            });
        })
        .catch(err => {
            console.error('Error loading properties:', err);
            select.innerHTML = '<option value="">Error loading properties</option>';
        });
}

function setupExplainButton() {
    const explainButton = document.getElementById('explain-button');
    const explainResult = document.getElementById('explain-result');
    const select = document.getElementById('property-select');

    if (!explainButton || !explainResult || !select) return;

    explainButton.addEventListener('click', async function() {
        const selectedId = select.value;
        if (!selectedId) {
            alert('Please select a property first.');
            return;
        }

        // Show initial loading state
        explainResult.style.display = 'block';
        explainResult.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <div class="loading-text">Analyzing property data...</div>
            </div>
        `;
        explainButton.disabled = true;
        explainButton.textContent = 'Analyzing...';

        try {
            const response = await fetch('http://localhost:5000/explain_prediction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ property_index: parseInt(selectedId) })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();

            if (data.error) {
                explainResult.innerHTML = `<div class="error-message">${data.error}</div>`;
                return;
            }

            // Build HTML for explanation
            let html = `
                <div class="explanation-container fade-in">
                    <div class="summary-section">
                        <h3>Property Analysis Summary</h3>
                        <div class="summary-text">${data.summary_text}</div>
                        <div class="price-display">
                            <span class="predicted-price">Predicted Price: $${parseFloat(data.predicted_price).toLocaleString()}</span>
                        </div>
                    </div>
                    <div class="scores-section">
                        <h4>Quality Scores</h4>
                        <div class="scores-grid">
                            <div class="score-item">
                                <span class="score-label">Neighborhood:</span>
                                <span class="score-value">${parseFloat(data.scores.neighborhood).toFixed(2)}/10</span>
                            </div>
                            <div class="score-item">
                                <span class="score-label">Accessibility:</span>
                                <span class="score-value">${parseFloat(data.scores.accessibility).toFixed(2)}/10</span>
                            </div>
                            <div class="score-item">
                                <span class="score-label">Green Space:</span>
                                <span class="score-value">${parseFloat(data.scores.green_space).toFixed(2)}/10</span>
                            </div>
                        </div>
                    </div>
                    <div class="charts-section">
                        <h4>Visual Analysis</h4>
            `;

            data.charts.forEach((chart, index) => {
                html += `
                    <div class="chart-container" data-chart-index="${index}">
                        <h5 class="chart-title">${chart.title}</h5>
                        <div class="chart-loading" id="loading-${index}">
                            <div class="chart-spinner"></div>
                            <span class="loading-text">Loading chart...</span>
                        </div>
                        <div class="chart-content">
                            <img src="${chart.url}" 
                                 alt="${chart.title}" 
                                 class="chart-image"
                                 data-chart-index="${index}"
                                 onload="handleChartLoad(${index})"
                                 onerror="handleChartError(${index})"
                                 style="opacity:0;">
                            <p class="chart-description">${chart.description}</p>
                        </div>
                    </div>
                `;
            });

            html += `</div></div>`; // close charts and container

            explainResult.style.opacity = '0';
            setTimeout(() => {
                explainResult.innerHTML = html;
                explainResult.style.opacity = '1';
            }, 100);

        } catch (err) {
            console.error('Error generating explanation:', err);
            explainResult.innerHTML = `
                <div class="error-container">
                    <div class="error-icon">🚀</div>
                    <div class="error-title">Connection Lost</div>
                    <div class="error-message">Unable to connect to analysis service. Please try again.</div>
                    <button class="retry-button" onclick="setupExplainButton(); explainButton.click()">Retry</button>
                </div>
            `;
        } finally {
            explainButton.disabled = false;
            explainButton.textContent = 'Explain Selection';
        }
    });
}

function handleChartLoad(index) {
    const chartContainer = document.querySelector(`.chart-container[data-chart-index="${index}"]`);
    if (chartContainer) {
        // Hide the loading spinner
        const loadingElement = chartContainer.querySelector('.chart-loading');
        if (loadingElement) loadingElement.style.display = 'none';

        // Show the description text
        const description = chartContainer.querySelector('.chart-description');
        if (description) description.style.display = 'block';

        // Fade in the image
        const chartImage = chartContainer.querySelector('img');
        if (chartImage) {
            chartImage.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            chartImage.style.opacity = '1';
            chartImage.style.transform = 'translateY(0)';
        }
    }
}

function handleChartError(index) {
    const chartContainer = document.querySelector(`.chart-container[data-chart-index="${index}"]`);
    if (chartContainer) {
        // Hide the description text
        const description = chartContainer.querySelector('.chart-description');
        if (description) description.style.display = 'none';

        // Replace the loading spinner with an error message
        const loadingElement = chartContainer.querySelector('.chart-loading');
        if (loadingElement) {
            loadingElement.innerHTML = `
                <div class="chart-error">
                    <span class="error-icon">⚠️</span>
                    <span class="error-text">Chart failed to load</span>
                    <button class="retry-chart-btn" onclick="retryChart(${index})">Retry</button>
                </div>
            `;
        }
        
        // Ensure the main image tag is hidden
        const chartImage = chartContainer.querySelector('img');
        if (chartImage) {
            chartImage.style.display = 'none';
        }
    }
}

function retryChart(index) {
    const chartContainer = document.querySelector(`.chart-container[data-chart-index="${index}"]`);
    if(chartContainer) {
        const loadingElement = chartContainer.querySelector('.chart-loading');
        const chartImage = chartContainer.querySelector('img');
        
        loadingElement.innerHTML = `
            <div class="chart-loading">
                <div class="chart-spinner"></div>
                <span class="loading-text">Retrying chart...</span>
            </div>
        `;
        loadingElement.style.display = 'flex';
        loadingElement.style.opacity = '1';
        
        if (chartImage) {
            chartImage.style.display = 'block';
            chartImage.style.opacity = '0';
            const currentSrc = chartImage.src.split('?')[0];
            chartImage.src = `${currentSrc}?t=${new Date().getTime()}`;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadProperties();
    setupExplainButton();
});