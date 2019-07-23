importScripts('https://www.gstatic.com/firebasejs/6.3.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/6.3.1/firebase-messaging.js');

// Initialize Firebase
  var firebaseConfig = {
    apiKey: "AIzaSyBTVn4tvZurN7aBif9zUtEr61fooLK7LkE",
    authDomain: "cnunotice-2619e.firebaseapp.com",
    databaseURL: "https://cnunotice-2619e.firebaseio.com",
    projectId: "cnunotice-2619e",
    storageBucket: "",
    messagingSenderId: "56777081777",
    appId: "1:56777081777:web:fa0923a982e610b0"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function(payload){

    const title = "HelloWorld";
    const options = {
            body: payload.data.status
    };

    return self.registration.showNotification(title,options);
});

