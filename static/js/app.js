Vue.component('line-chart', {
    extends: VueChartJs.Line,
    props: ['labels', 'values', 'title'],
    mounted() {
        const data = {
            labels: Array.from(Array(this.values.length).keys()),
            datasets: [{
                label: this.title,
                data: this.values,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        }
        this.renderChart(data, {
            responsive: true
        })
    }
})

new Vue({
    el: '#app',
    data: {
        results: null,
        error: null,
        loading: false,
        tab: null,
        viewAs: 'chart',
    },
    computed: {
        tabs () {
            return Array.from((new Set(this.results.map(r => r.name))).values());
        },
        tabResults () {
            return this.results.filter(r => r.name === this.tab);
        },
        tableCols () {
            return [
                'name',
                'version',
                'file',
                'duration',
                'cpu_usage',
                'ram',
                'available_memory',
            ]
        },
        durationData () {
            return  this.results.map(result => result.duration);
        },
        cpuData () {
            return  this.results.map(result => result.duration);
        },
        ramData () {
            return  this.results.map(result => result.duration);
        },
        availableMemoryData () {
            return  this.results.map(result => result.duration);
        },
    },
    methods: {
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
                    this.tab = this.tabs[0];
                })
                .catch(error => {
                    this.loading = false;
                    console.error(error);
                    alert('Unknown error');
                });
        }
    }
})