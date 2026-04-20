/**
 * Nawawi's 40 Hadiths - Enhanced Player with Transliteration Support
 * Extends HadithPlayerEnhanced with real-time transliteration display and highlighting
 * 
 * Features:
 * - Real-time word highlighting synchronized with audio playback
 * - Transliteration text display alongside original Arabic
 * - Click-to-seek functionality on words
 * - Auto-scroll to current word
 * - Playback speed control
 * - Word statistics and search
 * - Mobile-first responsive design
 */

class HadithPlayerWithTransliteration extends HadithPlayerEnhanced {
    constructor(containerId, transliterationContainerId, options = {}) {
        super(containerId, options);
        
        this.transliterationContainer = document.getElementById(transliterationContainerId);
        if (!this.transliterationContainer) {
            console.warn(`Transliteration container with ID "${transliterationContainerId}" not found`);
        }
        
        this.transliterationData = null;
        this.showTransliteration = options.showTransliteration !== false;
        this.transliterationLanguage = options.transliterationLanguage || 'transliteration';
    }

    /**
     * Load hadith data with transliteration
     * @param {number} hadithNumber 
     * @param {string} language 'en' or 'ar'
     */
    async loadHadith(hadithNumber, language = 'en') {
        this.language = language;
        this.currentHadithNumber = hadithNumber;
        
        try {
            // Fetch full hadith data from the API
            const response = await fetch(`${this.apiBaseUrl}/hadiths/${hadithNumber}/full`);
            if (!response.ok) throw new Error('Failed to fetch hadith data');
            
            const data = await response.json();
            
            // Select the appropriate audio and sync data based on language
            const audioInfo = language === 'ar' ? data.audio.arabic : data.audio.english;
            
            this.audio.src = audioInfo.url;
            this.syncData = audioInfo.sync;
            
            // Fetch transliteration data
            try {
                const transResponse = await fetch(`${this.apiBaseUrl}/transliterations/${hadithNumber}`);
                if (transResponse.ok) {
                    this.transliterationData = await transResponse.json();
                }
            } catch (error) {
                console.warn('Could not fetch transliteration data:', error);
            }
            
            // Reset statistics
            this.stats.totalWords = this.syncData?.words?.length || 0;
            this.stats.wordsSpoken = 0;
            
            this.renderText();
            this.renderTransliteration();
        } catch (error) {
            console.error('Error loading hadith:', error);
            throw error;
        }
    }

    /**
     * Render the transliteration text
     */
    renderTransliteration() {
        if (!this.transliterationContainer || !this.transliterationData) return;
        
        this.transliterationContainer.innerHTML = '';
        this.transliterationContainer.className = `hadith-transliteration-container ${this.language === 'ar' ? 'rtl' : 'ltr'}`;
        
        // Create a header
        const header = document.createElement('div');
        header.className = 'transliteration-header';
        header.innerHTML = `
            <h3>Arabic Transliteration</h3>
            <p class="transliteration-meta">${this.transliterationData.title}</p>
        `;
        this.transliterationContainer.appendChild(header);
        
        // Create the transliteration text display
        const textDiv = document.createElement('div');
        textDiv.className = 'transliteration-text';
        textDiv.textContent = this.transliterationData.Arabic_Transliteration_text;
        this.transliterationContainer.appendChild(textDiv);
        
        // Create word-by-word breakdown if sync data exists
        if (this.syncData && this.syncData.words) {
            const wordsDiv = document.createElement('div');
            wordsDiv.className = 'transliteration-words';
            
            this.syncData.words.forEach((wordObj, index) => {
                const span = document.createElement('span');
                span.id = `trans-word-${index}`;
                span.className = 'transliteration-word';
                span.textContent = wordObj.word + ' ';
                span.dataset.index = index;
                span.dataset.start = wordObj.start;
                span.dataset.end = wordObj.end;
                
                // Allow clicking a word to seek audio
                span.addEventListener('click', () => this.seekToWord(index));
                
                wordsDiv.appendChild(span);
            });
            
            this.transliterationContainer.appendChild(wordsDiv);
        }
    }

    /**
     * Override updateHighlighting to also update transliteration highlighting
     */
    updateHighlighting() {
        if (!this.syncData || !this.syncData.words) return;

        const currentTime = this.audio.currentTime;
        let foundWord = false;
        
        this.syncData.words.forEach((wordObj, index) => {
            const wordElement = document.getElementById(`word-${index}`);
            const transWordElement = document.getElementById(`trans-word-${index}`);
            
            if (currentTime >= wordObj.start && currentTime < wordObj.end) {
                if (wordElement && !wordElement.classList.contains('highlighted')) {
                    // Remove highlight from previous word
                    document.querySelectorAll('.hadith-word.highlighted').forEach(el => {
                        el.classList.remove('highlighted');
                    });
                    document.querySelectorAll('.transliteration-word.highlighted').forEach(el => {
                        el.classList.remove('highlighted');
                    });
                    
                    // Add highlight to current word
                    if (wordElement) wordElement.classList.add('highlighted');
                    if (transWordElement) transWordElement.classList.add('highlighted');
                    
                    this.currentWordIndex = index;
                    this.stats.wordsSpoken = index + 1;
                    
                    // Auto-scroll to the active word if it's not visible
                    if (this.autoScroll) {
                        if (wordElement) this.scrollToWord(wordElement);
                        if (transWordElement) this.scrollToWord(transWordElement);
                    }
                    
                    foundWord = true;
                    
                    if (this.onTimeUpdate) {
                        this.onTimeUpdate({
                            currentTime,
                            wordIndex: index,
                            word: wordObj.word,
                            stats: this.getStats()
                        });
                    }
                }
            }
        });
        
        if (!foundWord && this.currentWordIndex >= 0) {
            this.currentWordIndex = -1;
        }
    }

    /**
     * Export data including transliteration
     */
    exportData() {
        return {
            hadith_number: this.currentHadithNumber,
            language: this.language,
            sync_data: this.syncData,
            transliteration: this.transliterationData,
            audio_url: this.audio.src,
            stats: this.getStats()
        };
    }
}
