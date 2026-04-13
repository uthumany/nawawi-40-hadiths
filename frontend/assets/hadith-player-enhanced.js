/**
 * Nawawi's 40 Hadiths - Enhanced Word-by-Word Highlighting Player
 * Supports both Arabic and English versions with advanced synchronization features.
 * 
 * Features:
 * - Real-time word highlighting synchronized with audio playback
 * - Click-to-seek functionality on words
 * - Auto-scroll to current word
 * - Playback speed control
 * - Word statistics and search
 * - Responsive design for mobile and desktop
 */

class HadithPlayerEnhanced {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container with ID "${containerId}" not found`);
        }
        
        this.audio = new Audio();
        this.syncData = null;
        this.language = options.language || 'en'; // 'en' or 'ar'
        this.apiBaseUrl = options.apiBaseUrl || '/';
        this.onWordClick = options.onWordClick || null;
        this.onTimeUpdate = options.onTimeUpdate || null;
        this.autoScroll = options.autoScroll !== false;
        this.highlightColor = options.highlightColor || '#4caf50';
        
        // Player state
        this.currentHadithNumber = null;
        this.currentWordIndex = -1;
        this.isPlaying = false;
        this.playbackRate = 1.0;
        
        // Statistics
        this.stats = {
            totalWords: 0,
            wordsSpoken: 0,
            startTime: null,
            endTime: null
        };
        
        this.init();
    }

    init() {
        this.audio.addEventListener('timeupdate', () => this.updateHighlighting());
        this.audio.addEventListener('play', () => {
            this.isPlaying = true;
            this.stats.startTime = Date.now();
        });
        this.audio.addEventListener('pause', () => {
            this.isPlaying = false;
        });
        this.audio.addEventListener('ended', () => {
            this.isPlaying = false;
            this.stats.endTime = Date.now();
        });
    }

    /**
     * Load hadith data and prepare the player
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
            
            // Reset statistics
            this.stats.totalWords = this.syncData?.words?.length || 0;
            this.stats.wordsSpoken = 0;
            
            this.renderText();
        } catch (error) {
            console.error('Error loading hadith:', error);
            throw error;
        }
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
            span.dataset.index = index;
            span.dataset.start = wordObj.start;
            span.dataset.end = wordObj.end;
            
            // Allow clicking a word to seek audio
            span.addEventListener('click', () => this.seekToWord(index));
            
            // Add hover tooltip with timing information
            span.addEventListener('mouseenter', (e) => {
                this.showWordTooltip(e, wordObj, index);
            });
            
            this.container.appendChild(span);
        });
    }

    /**
     * Show tooltip with word timing information
     */
    showWordTooltip(event, wordObj, index) {
        const tooltip = document.createElement('div');
        tooltip.className = 'hadith-word-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-content">
                <div class="tooltip-word">${wordObj.word}</div>
                <div class="tooltip-time">${this.formatTime(wordObj.start)} - ${this.formatTime(wordObj.end)}</div>
                <div class="tooltip-index">Word #${index + 1}</div>
            </div>
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = event.target.getBoundingClientRect();
        tooltip.style.left = (rect.left + rect.width / 2) + 'px';
        tooltip.style.top = (rect.top - 10) + 'px';
        
        event.target.addEventListener('mouseleave', () => {
            tooltip.remove();
        });
    }

    /**
     * Seek to a specific word and play from that point
     */
    seekToWord(wordIndex) {
        if (wordIndex < 0 || wordIndex >= this.syncData.words.length) return;
        
        const wordObj = this.syncData.words[wordIndex];
        this.audio.currentTime = wordObj.start;
        
        if (this.audio.paused) {
            this.audio.play();
        }
        
        if (this.onWordClick) {
            this.onWordClick(wordObj, wordIndex);
        }
    }

    /**
     * Update the highlighting based on current audio time
     */
    updateHighlighting() {
        if (!this.syncData || !this.syncData.words) return;

        const currentTime = this.audio.currentTime;
        let foundWord = false;
        
        this.syncData.words.forEach((wordObj, index) => {
            const wordElement = document.getElementById(`word-${index}`);
            if (!wordElement) return;

            if (currentTime >= wordObj.start && currentTime < wordObj.end) {
                if (!wordElement.classList.contains('highlighted')) {
                    // Remove highlight from previous word
                    document.querySelectorAll('.hadith-word.highlighted').forEach(el => {
                        el.classList.remove('highlighted');
                    });
                    
                    wordElement.classList.add('highlighted');
                    this.currentWordIndex = index;
                    this.stats.wordsSpoken = index + 1;
                    
                    // Auto-scroll to the active word if it's not visible
                    if (this.autoScroll) {
                        this.scrollToWord(wordElement);
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
     * Scroll to a word element smoothly
     */
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

    /**
     * Format time in MM:SS format
     */
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    /**
     * Get current playback statistics
     */
    getStats() {
        return {
            ...this.stats,
            currentTime: this.audio.currentTime,
            duration: this.audio.duration,
            progress: (this.audio.currentTime / this.audio.duration) * 100
        };
    }

    /**
     * Search for words in the hadith
     */
    searchWords(query) {
        if (!this.syncData || !this.syncData.words) return [];
        
        const queryLower = query.toLowerCase();
        const results = [];
        
        this.syncData.words.forEach((wordObj, index) => {
            if (wordObj.word.toLowerCase().includes(queryLower)) {
                results.push({
                    index,
                    word: wordObj.word,
                    start: wordObj.start,
                    end: wordObj.end
                });
            }
        });
        
        return results;
    }

    /**
     * Highlight search results
     */
    highlightSearchResults(query) {
        const results = this.searchWords(query);
        
        // Clear previous search highlights
        document.querySelectorAll('.hadith-word.search-highlight').forEach(el => {
            el.classList.remove('search-highlight');
        });
        
        // Add search highlights
        results.forEach(result => {
            const element = document.getElementById(`word-${result.index}`);
            if (element) {
                element.classList.add('search-highlight');
            }
        });
        
        return results;
    }

    /**
     * Set playback speed
     */
    setPlaybackSpeed(rate) {
        this.playbackRate = rate;
        this.audio.playbackRate = rate;
    }

    /**
     * Get current playback speed
     */
    getPlaybackSpeed() {
        return this.playbackRate;
    }

    /**
     * Get word at specific time
     */
    getWordAtTime(timeSeconds) {
        if (!this.syncData || !this.syncData.words) return null;
        
        for (let i = 0; i < this.syncData.words.length; i++) {
            const wordObj = this.syncData.words[i];
            if (timeSeconds >= wordObj.start && timeSeconds < wordObj.end) {
                return {
                    index: i,
                    word: wordObj.word,
                    start: wordObj.start,
                    end: wordObj.end
                };
            }
        }
        
        return null;
    }

    /**
     * Get word by index
     */
    getWord(index) {
        if (!this.syncData || !this.syncData.words || index < 0 || index >= this.syncData.words.length) {
            return null;
        }
        
        const wordObj = this.syncData.words[index];
        return {
            index,
            word: wordObj.word,
            start: wordObj.start,
            end: wordObj.end
        };
    }

    /**
     * Get surrounding words (context)
     */
    getWordContext(index, contextSize = 3) {
        if (!this.syncData || !this.syncData.words) return null;
        
        const words = this.syncData.words;
        const start = Math.max(0, index - contextSize);
        const end = Math.min(words.length, index + contextSize + 1);
        
        return {
            before: words.slice(start, index).map((w, i) => ({
                index: start + i,
                word: w.word
            })),
            current: {
                index,
                word: words[index].word,
                start: words[index].start,
                end: words[index].end
            },
            after: words.slice(index + 1, end).map((w, i) => ({
                index: index + 1 + i,
                word: w.word
            }))
        };
    }

    /**
     * Export current hadith data
     */
    exportData() {
        return {
            hadith_number: this.currentHadithNumber,
            language: this.language,
            sync_data: this.syncData,
            audio_url: this.audio.src,
            stats: this.getStats()
        };
    }

    // Playback controls
    play() { 
        this.audio.play(); 
    }
    
    pause() { 
        this.audio.pause(); 
    }
    
    stop() {
        this.audio.pause();
        this.audio.currentTime = 0;
        this.currentWordIndex = -1;
        document.querySelectorAll('.hadith-word.highlighted').forEach(el => {
            el.classList.remove('highlighted');
        });
    }
    
    setCurrentTime(seconds) {
        this.audio.currentTime = seconds;
    }
    
    getCurrentTime() {
        return this.audio.currentTime;
    }
    
    getDuration() {
        return this.audio.duration;
    }
    
    setVolume(volume) {
        this.audio.volume = Math.max(0, Math.min(1, volume));
    }
    
    getVolume() {
        return this.audio.volume;
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HadithPlayerEnhanced;
}
