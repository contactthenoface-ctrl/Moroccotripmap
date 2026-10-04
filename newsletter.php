<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);

    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $to = "contact@kamliseo.com";
        $subject = "Nouvelle inscription à la Newsletter";
        $message = "Un nouvel utilisateur s'est inscrit à la newsletter : " . $email;
        $headers = "From: no-reply@moroccotripmap.com\r\n" .
                   "Reply-To: " . $email . "\r\n" .
                   "Content-Type: text/plain; charset=UTF-8\r\n";

        if (mail($to, $subject, $message, $headers)) {
            header("Location: index.html?status=success");
        } else {
            header("Location: index.html?status=error");
        }
    } else {
        header("Location: index.html?status=invalid");
    }
    exit();
}
?>
