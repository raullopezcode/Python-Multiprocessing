Vue.component('line-chart', {
    extends: VueChartJs.Line,
    props: ['dataset', 'title'],
    watch: {
        dataset (newVal) {
            this.render()
        }
    },
    mounted() {
        this.render()
    },
    methods: {
        render() {
            const data = {
                labels: Array.from(Array(this.dataset[0].data.length).keys()),
                datasets: this.dataset
            }
    
            this.renderChart(data, {
                responsive: true,
                title: {
                    display: true,
                    text: this.title
                }
            })
        }
    }
})

new Vue({
    el: '#app',
    data: {
        results: null,
        error: null,
        loading: false,
        tab: null,
        tabs: [],
        viewAs: 'chart',
    },
    computed: {
        tabResults () {
            return this.results.filter(r => r.name === this.tab);
        },
        tableCols () {
            return [
                'name',
                'option',
                'version',
                'file',
                'duration',
                'cpu_usage',
                'ram',
                'available_memory',
            ];
        },
        durationDatasets () {
            return this.dataset('duration')
        },
        cpuDatasets () {
            return this.dataset('cpu_usage')
        },
        ramDatasets () {
            return this.dataset('ram')
        },
        availableMemoryDatasets () {
            return this.dataset('available_memory')
        },
    },
    methods: {
        dataset(key) {
            const options = Array.from(new Set(this.tabResults.map(result => result.option)));
            const datasets = [];
            let i = 0;
            for (const option of options) {
                datasets.push({
                    label: option,
                    data: this.tabResults.filter(result => result.option === option).map(item => item[key]),
                    fill: false,
                    borderColor: this.getColor(i, options.length),
                    tension: 0.1
                });
                i += 1;
            }

            return datasets;
        },
        send() {
            if (this.loading) {
                return;
            }

            this.loading = true;
            this.results = null;
            const form = document.getElementById('test-form');
            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    this.loading = false;
                    if (data.error) {
                        this.error = data.error;
                        return;
                    }
    
                    this.error = null;
                    this.results = data.results;
                    this.tabs = Array.from((new Set(this.results.map(r => r.name))).values());
                    this.tab = this.tabs[0];
                })
                .catch(error => {
                    this.loading = false;
                    console.error(error);
                    alert('Unknown error');
                });
        },
        getColor(i, maxColors) { 
            return chroma.scale(['#00ddba', '#0a5edf', '#e84364']).colors(maxColors)[i];
        }
    }
})