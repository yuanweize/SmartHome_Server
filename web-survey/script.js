document.addEventListener('DOMContentLoaded', () => {
    const nextBtns = document.querySelectorAll('.next-btn');
    const prevBtns = document.querySelectorAll('.prev-btn');
    const groups = document.querySelectorAll('.question-group');
    const progressBar = document.getElementById('progress');
    const form = document.getElementById('survey-form');
    const totalSteps = groups.length - 1; // Subtract 1 for success screen

    // Function to validate current step before proceeding
    function validateStep(stepIndex) {
        const currentGroup = document.getElementById(`step-${stepIndex}`);
        if (!currentGroup) return true;

        const inputs = currentGroup.querySelectorAll('input[required]');
        let isValid = true;

        // Group radio buttons by name to check if at least one is selected
        const radioGroups = {};
        
        inputs.forEach(input => {
            if (input.type === 'radio') {
                if (!radioGroups[input.name]) {
                    radioGroups[input.name] = [];
                }
                radioGroups[input.name].push(input);
            } else if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '';
            }
        });

        // Check radio groups
        for (const groupName in radioGroups) {
            const isChecked = radioGroups[groupName].some(radio => radio.checked);
            if (!isChecked) {
                isValid = false;
                // Highlight the cards containing the unchecked required radios
                radioGroups[groupName].forEach(radio => {
                    const card = radio.closest('.radio-card') || radio.parentElement;
                    card.style.outline = '1px solid red';
                    setTimeout(() => card.style.outline = '', 2000);
                });
            }
        }

        return isValid;
    }

    // Navigation logic
    function goToStep(targetIndex) {
        groups.forEach(g => g.classList.remove('active'));
        document.getElementById(`step-${targetIndex}`).classList.add('active');
        
        // Update progress bar (don't count step 0 or success screen)
        if (targetIndex === 0) {
            progressBar.style.width = '0%';
        } else if (targetIndex === 'success') {
            progressBar.style.width = '100%';
            progressBar.style.backgroundColor = 'var(--success)';
        } else {
            const progress = (targetIndex / (totalSteps - 1)) * 100;
            progressBar.style.width = `${progress}%`;
        }
    }

    // Next buttons
    nextBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const currentStep = e.target.closest('.question-group').id.replace('step-', '');
            const targetStep = e.target.dataset.target;
            
            if (currentStep === '0' || validateStep(currentStep)) {
                goToStep(targetStep);
            } else {
                alert('Prosím vyplňte všechny povinné otázky před pokračováním.');
            }
        });
    });

    // Prev buttons
    prevBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetStep = e.target.dataset.target;
            goToStep(targetStep);
        });
    });

    // Slider logic
    const slider = document.getElementById('localSlider');
    const valDisplay = document.getElementById('localVal');
    if(slider) {
        slider.addEventListener('input', (e) => {
            valDisplay.textContent = e.target.value;
        });
    }

    // Form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (validateStep(4)) { // Validate last step
            // Here you would normally send the FormData to a server/API
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            console.log('Survey Data Submitted:', data);
            
            // Show success screen
            goToStep('success');
        } else {
            alert('Prosím vyplňte všechny povinné otázky.');
        }
    });

    // Add PSM logic validation (cheap cannot be > expensive)
    const psmInputs = document.querySelectorAll('.input-with-currency input');
    psmInputs.forEach(input => {
        input.addEventListener('blur', () => {
            // Optional: add visual feedback if logic is broken (e.g. too_cheap > too_expensive)
        });
    });
});
