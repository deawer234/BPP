const eventLog = document.getElementById("event-log");
window.addEventListener("load", showEventLog);
var eventLogCookie = [];

export function showEventLog() {
    // Retrieve the cookie value
    console.log("here");
    const cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)array\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    // Parse the cookie value back into an array
    if (cookieValue) {
        const eventArray = JSON.parse(decodeURIComponent(cookieValue));

        // Filter out expired entries
        const filteredEventArray = eventArray.filter(entry => !isEntryExpired(entry));

        // Display the event log
        filteredEventArray.forEach(element => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.innerHTML = `${element.content}`;
            eventLog.appendChild(li);
        });

        // Remove expired entries and update the cookie
        removeExpiredEntries(filteredEventArray);
    }
}

function isEntryExpired(entry) {
    const currentTime = new Date().getTime();
    return currentTime > entry.expiration;
}

function removeExpiredEntries(filteredEventArray) {
    eventLogCookie = filteredEventArray;
    document.cookie = `array=${encodeURIComponent(JSON.stringify(eventLogCookie))}; expires=Tue, 18 Apr 2023 00:30:00 UTC; path=/`;
}

export function appendToEventLog(message) {
    const li = document.createElement("li");
    li.className = "list-group-item";
    const time = new Date();
    li.innerHTML = `<small class="text-muted">${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}</small><br>${message}`;
    eventLog.appendChild(li);

    const existingCookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)array\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    if (existingCookieValue) {
        eventLogCookie = JSON.parse(decodeURIComponent(existingCookieValue));
    }

    // Set the entry to expire in half an hour
    const expirationDate = new Date();
    expirationDate.setMinutes(expirationDate.getMinutes() + 20);

    const entry = {
        content: `<small class="text-muted">${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}</small><br>${message}`,
        expiration: expirationDate.getTime()
    };

    eventLogCookie.push(entry);

    // Remove expired entries and update the cookie
    const filteredEventArray = eventLogCookie.filter(entry => !isEntryExpired(entry));
    removeExpiredEntries(filteredEventArray);

    // Scroll to the bottom of the eventLog element
    eventLog.scrollTop = eventLog.scrollHeight;
}
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}