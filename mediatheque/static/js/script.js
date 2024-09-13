document.addEventListener('DOMContentLoaded', function() {
            const typeSelect = document.getElementById('type_media');
            const realisateurField = document.getElementById('realisateur_field');
            const auteurField = document.getElementById('auteur_field');
            const artisteField = document.getElementById('artiste_field');
            const createurField = document.getElementById('createur_field');

            typeSelect.addEventListener('change', function() {
                const type = this.value;
                realisateurField.style.display = type === 'DVD' ? 'block' : 'none';
                auteurField.style.display = type === 'Livre' ? 'block' : 'none';
                artisteField.style.display = type === 'CD' ? 'block' : 'none';
                createurField.style.display = type === 'JeuDePlateau' ? 'block' : 'none';
            });

            typeSelect.dispatchEvent(new Event('change'));
        });