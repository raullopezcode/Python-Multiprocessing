new Vue({
    el: '#app',
    data: {
        results: null,
        error: null,
        loading: false,
        tab: null,
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
        }
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