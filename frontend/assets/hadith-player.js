/**
 * Nawawi's 40 Hadiths - Word-by-Word Highlighting Implementation
 * Supports both Arabic and English versions.
 */

class HadithPlayer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.audio = new Audio();
        this.syncData = null;
        this.language = options.language || 'en'; // 'en' or 'ar'
        this.onWordClick = options.onWordClick || null;
        
        this.init();
    }

    init() {
        this.audio.addEventListener('timeupdate', () => this.updateHighlighting());
    }

    /**
     * Load hadith data and prepare the player
     * @param {number} hadithNumber 
     * @param {string} language 'en' or 'ar'
     */
    async loadHadith(hadithNumber, language = 'en') {
        this.language = language;
        
        // Fetch full hadith data from the API
        const response = await fetch(`/hadiths/${hadithNumber}/full`);
        if (!response.ok) throw new Error('Failed to fetch hadith data');
        
        const data = await response.json();
        
        // Select the appropriate audio and sync data based on language
        const audioInfo = language === 'ar' ? data.audio.arabic : data.audio.english;
        
        this.audio.src = audioInfo.url;
        this.syncData = audioInfo.sync;
        
        this.renderText();
    }

    /**
     * Render the hadith text as individual word spans
     */
    renderText() {
        if (!this.syncData || !this.syncData.words) return;

        this.container.innerHTML = '';
        this.container.className = `hadith-text-container ${this.language === 'ar' ? 'rtl' : 'ltr'}`;
        
        this.syncData.words.forEach((wordObj, index) => {
            const span = document.createElement('span');
            span.id = `word-${index}`;
            span.className = 'hadith-word';
            span.textContent = wordObj.word + ' ';
            
            // Allow clicking a word to seek audio
            span.addEventListener('click', () => {
                this.audio.currentTime = wordObj.start;
                if (this.audio.paused) this.audio.play();
                if (this.onWordClick) this.onWordClick(wordObj, index);
            });
            
            this.container.appendChild(span);
        });
    }

    /**
     * Update the highlighting based on current audio time
     */
    updateHighlighting() {
        if (!this.syncData || !this.syncData.words) return;

        const currentTime = this.audio.currentTime;
        
        this.syncData.words.forEach((wordObj, index) => {
            const wordElement = document.getElementById(`word-${index}`);
            if (!wordElement) return;

            if (currentTime >= wordObj.start && currentTime < wordObj.end) {
                if (!wordElement.classList.contains('highlighted')) {
                    wordElement.classList.add('highlighted');
                    
                    // Auto-scroll to the active word if it's not visible
                    this.scrollToWord(wordElement);
                }
            } else {
                wordElement.classList.remove('highlighted');
            }
        });
    }

    scrollToWord(element) {
        const containerRect = this.container.getBoundingClientRect();
        const elementRect = element.getBoundingClientRect();

        if (elementRect.bottom > containerRect.bottom || elementRect.top < containerRect.top) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }
    }

    play() { this.audio.play(); }
    pause() { this.audio.pause(); }
    stop() {
        this.audio.pause();
        this.audio.currentTime = 0;
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HadithPlayer;
}
