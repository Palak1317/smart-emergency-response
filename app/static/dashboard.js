/* =========================================================
   SMART EMERGENCY RESPONSE SYSTEM
   Dashboard JavaScript
   ========================================================= */


/* =========================================================
   GLOBAL DATA
   ========================================================= */

let locationsMap = {};


/* =========================================================
   GENERIC FETCH FUNCTION
   ========================================================= */

async function fetchData(url) {

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }

    return await response.json();
}


/* =========================================================
   LOAD LOCATIONS
   ========================================================= */

async function loadLocations() {

    try {

        const locations = await fetchData("/locations/");

        locationsMap = {};

        locations.forEach(location => {

            locationsMap[location.id] = location.name;

        });

        console.log("Locations loaded:", locations);

    } catch (error) {

        console.error("Unable to load locations:", error);

    }
}


/* =========================================================
   LOAD LOCATIONS INTO EMERGENCY FORM
   ========================================================= */

async function loadEmergencyLocations() {

    const locationSelect =
        document.getElementById("emergencyLocation");

    if (!locationSelect) {

        console.error(
            "Emergency location dropdown not found."
        );

        return;
    }


    try {

        const locations = await fetchData("/locations/");

        console.log(
            "Emergency form locations:",
            locations
        );


        locationSelect.innerHTML =
            '<option value="">Select location</option>';


        if (!locations || locations.length === 0) {

            locationSelect.innerHTML =
                '<option value="">No locations available</option>';

            return;
        }


        locations.forEach(location => {

            const option =
                document.createElement("option");

            option.value = location.id;

            option.textContent =
                location.name;

            locationSelect.appendChild(option);

        });


    } catch (error) {

        console.error(
            "Unable to load emergency locations:",
            error
        );

        locationSelect.innerHTML =
            '<option value="">Unable to load locations</option>';
    }
}


/* =========================================================
   CREATE BADGE
   ========================================================= */

function createBadge(text) {

    if (!text) {
        return "";
    }

    const value =
        String(text).toUpperCase();

    const className =
        value.toLowerCase().replace(" ", "_");

    return `
        <span class="badge badge-${className}">
            ${value}
        </span>
    `;
}


/* =========================================================
   CREATE EMERGENCY
   ========================================================= */

async function createEmergency() {

    const type =
        document.getElementById("emergencyType").value;

    const severity =
        document.getElementById("emergencySeverity").value;

    const locationId =
        document.getElementById("emergencyLocation").value;

    const description =
        document.getElementById("emergencyDescription").value;

    const message =
        document.getElementById("emergencyMessage");

    const button =
        document.querySelector(".create-emergency-btn");


    /* Validation */

    if (!type || !severity || !locationId) {

        message.textContent =
            "Please select emergency type, severity and location.";

        message.style.color = "#dc2626";

        return;
    }


    button.disabled = true;

    button.textContent = "Reporting...";

    message.textContent = "";


    try {

        const response = await fetch(
            "/emergencies/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    type: type,

                    severity: severity,

                    description:
                        description || null,

                    location_id:
                        Number(locationId),

                    reported_by: null
                })
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to create emergency"
            );
        }


        message.textContent =
            `Emergency #${data.id} created successfully.`;

        message.style.color = "#16a34a";


        /* Clear form */

        document.getElementById(
            "emergencyType"
        ).value = "";

        document.getElementById(
            "emergencySeverity"
        ).value = "";

        document.getElementById(
            "emergencyLocation"
        ).value = "";

        document.getElementById(
            "emergencyDescription"
        ).value = "";


        /* Reload dashboard */

        await loadDashboard();


    } catch (error) {

        console.error(
            "Emergency creation error:",
            error
        );

        message.textContent =
            `Failed to create emergency: ${error.message}`;

        message.style.color = "#dc2626";


    } finally {

        button.disabled = false;

        button.textContent =
            "Report Emergency";
    }
}


/* =========================================================
   LOAD EMERGENCIES
   ========================================================= */

async function loadEmergencies() {

    const emergencies =
        await fetchData("/emergencies/");


    /* Statistics */

    document.getElementById(
        "totalEmergencies"
    ).textContent = emergencies.length;


    document.getElementById(
        "criticalEmergencies"
    ).textContent =
        emergencies.filter(
            emergency =>
                emergency.severity === "CRITICAL"
        ).length;


    document.getElementById(
        "pendingEmergencies"
    ).textContent =
        emergencies.filter(
            emergency =>
                emergency.status === "PENDING"
        ).length;


    const table =
        document.getElementById("emergencyTable");


    if (emergencies.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="7" class="empty-message">
                    No emergencies found.
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML =
        emergencies.map(emergency => {

            const location =
                locationsMap[emergency.location_id]
                || `Location #${emergency.location_id}`;


            const reported =
                emergency.created_at
                ? new Date(
                    emergency.created_at
                  ).toLocaleString()
                : "N/A";


            let action = "";


            if (emergency.status === "PENDING") {

                action = `
                    <button
                        id="dispatch-${emergency.id}"
                        class="dispatch-btn"
                        onclick="dispatchEmergency(${emergency.id})"
                    >
                        Dispatch
                    </button>
                `;

            } else {

                action = `
                    <span style="color:#94a3b8;">
                        No action
                    </span>
                `;
            }


            return `
                <tr>

                    <td>
                        #${emergency.id}
                    </td>

                    <td>
                        ${emergency.type}
                    </td>

                    <td>
                        ${createBadge(
                            emergency.severity
                        )}
                    </td>

                    <td>
                        ${location}
                    </td>

                    <td>
                        ${createBadge(
                            emergency.status
                        )}
                    </td>

                    <td>
                        ${reported}
                    </td>

                    <td>
                        ${action}
                    </td>

                </tr>
            `;

        }).join("");
}


/* =========================================================
   DISPATCH EMERGENCY
   ========================================================= */

async function dispatchEmergency(emergencyId) {

    const button =
        document.getElementById(
            `dispatch-${emergencyId}`
        );


    if (button) {

        button.disabled = true;

        button.textContent =
            "Dispatching...";
    }


    try {

        const response =
            await fetch(
                `/dispatches/assign/${emergencyId}`,
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to dispatch emergency"
            );
        }


        alert(
            `Resource assigned successfully!\n\n` +

            `Resource: ${data.resource_name}\n` +

            `Type: ${data.resource_type}\n` +

            `Distance: ${data.distance} km\n` +

            `Estimated Time: ` +
            `${data.estimated_time_minutes} minutes`
        );


        await loadDashboard();


    } catch (error) {

        alert(
            `Dispatch failed:\n${error.message}`
        );


        if (button) {

            button.disabled = false;

            button.textContent =
                "Dispatch";
        }
    }
}


/* =========================================================
   LOAD RESOURCES
   ========================================================= */

async function loadResources() {

    const resources =
        await fetchData("/resources/");


    document.getElementById(
        "availableResources"
    ).textContent =
        resources.filter(
            resource =>
                resource.status === "AVAILABLE"
        ).length;


    const table =
        document.getElementById("resourceTable");


    if (resources.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="6" class="empty-message">
                    No resources found.
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML =
        resources.map(resource => {

            const location =
                locationsMap[resource.location_id]
                || `Location #${resource.location_id}`;


            return `
                <tr>

                    <td>
                        #${resource.id}
                    </td>

                    <td>
                        ${resource.name}
                    </td>

                    <td>
                        ${resource.type}
                    </td>

                    <td>
                        ${createBadge(
                            resource.status
                        )}
                    </td>

                    <td>
                        ${resource.capacity}
                    </td>

                    <td>
                        ${location}
                    </td>

                </tr>
            `;

        }).join("");
}


/* =========================================================
   UPDATE DISPATCH STATUS
   ========================================================= */

async function updateDispatchStatus(
    dispatchId,
    status
) {

    try {

        const response =
            await fetch(
                `/dispatches/${dispatchId}/status?status=${status}`,
                {
                    method: "PUT"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to update dispatch"
            );
        }


        await loadDashboard();


    } catch (error) {

        alert(
            `Status update failed:\n${error.message}`
        );
    }
}


/* =========================================================
   LOAD DISPATCHES
   ========================================================= */

async function loadDispatches() {

    const dispatches =
        await fetchData("/dispatches/");


    /* -----------------------------------------------------
       Count active dispatches
       ----------------------------------------------------- */

    const active =
        dispatches.filter(
            dispatch =>
                dispatch.status !== "RESOLVED"
        ).length;


    document.getElementById(
        "activeDispatches"
    ).textContent = active;


    const table =
        document.getElementById(
            "dispatchTable"
        );


    /* -----------------------------------------------------
       No dispatches
       ----------------------------------------------------- */

    if (
        !dispatches ||
        dispatches.length === 0
    ) {

        table.innerHTML = `
            <tr>
                <td
                    colspan="8"
                    class="empty-message"
                >
                    No dispatch records found.
                </td>
            </tr>
        `;

        return;
    }


    /* -----------------------------------------------------
       Create dispatch rows
       ----------------------------------------------------- */

    table.innerHTML =
        dispatches.map(dispatch => {


            /* ---------------------------------------------
               Determine action button
               --------------------------------------------- */

            let action = "";


            if (
                dispatch.status ===
                "DISPATCHED"
            ) {

                action = `
                    <button
                        class="status-btn"
                        onclick="updateDispatchStatus(
                            ${dispatch.id},
                            'EN_ROUTE'
                        )"
                    >
                        En Route
                    </button>
                `;


            } else if (
                dispatch.status ===
                "EN_ROUTE"
            ) {

                action = `
                    <button
                        class="status-btn"
                        onclick="updateDispatchStatus(
                            ${dispatch.id},
                            'ARRIVED'
                        )"
                    >
                        Arrived
                    </button>
                `;


            } else if (
                dispatch.status ===
                "ARRIVED"
            ) {

                action = `
                    <button
                        class="status-btn"
                        onclick="updateDispatchStatus(
                            ${dispatch.id},
                            'RESOLVED'
                        )"
                    >
                        Resolve
                    </button>
                `;


            } else if (
                dispatch.status ===
                "RESOLVED"
            ) {

                action = `
                    <span
                        style="
                            color:#16a34a;
                            font-weight:600;
                        "
                    >
                        Completed
                    </span>
                `;


            } else {

                action = `
                    <span
                        style="
                            color:#64748b;
                        "
                    >
                        ${dispatch.status}
                    </span>
                `;
            }


            /* ---------------------------------------------
               Emergency display
               --------------------------------------------- */

            const emergencyText =

                `<strong>
                    #${dispatch.emergency_id}
                </strong>`;



            const emergencyDetails =

                dispatch.emergency_type
                    ? dispatch.emergency_type
                    : "Unknown";



            const emergencySeverity =

                dispatch.emergency_severity
                    ? createBadge(
                        dispatch.emergency_severity
                    )
                    : "";


            /* ---------------------------------------------
               Resource display
               --------------------------------------------- */

            const resourceName =

                dispatch.resource_name
                    || `Resource #${dispatch.resource_id}`;


            const resourceType =

                dispatch.resource_type
                    ? dispatch.resource_type
                    : "Unknown";


            /* ---------------------------------------------
               Route display
               --------------------------------------------- */

            let routeHTML = "";


            if (
                dispatch.route_names &&
                dispatch.route_names.length > 0
            ) {

                routeHTML = `

                    <div class="route-path">

                        ${dispatch.route_names
                            .map(
                                (location, index) => {

                                    if (
                                        index ===
                                        dispatch.route_names.length - 1
                                    ) {

                                        return `
                                            <span
                                                class="route-location"
                                            >
                                                ${location}
                                            </span>
                                        `;
                                    }


                                    return `
                                        <span
                                            class="route-location"
                                        >
                                            ${location}
                                        </span>

                                        <span
                                            class="route-arrow"
                                        >
                                            →
                                        </span>
                                    `;
                                }
                            )
                            .join("")}

                    </div>

                `;

            } else {

                routeHTML = `
                    <span
                        class="route-unavailable"
                    >
                        Route unavailable
                    </span>
                `;
            }


            /* ---------------------------------------------
               Distance
               --------------------------------------------- */

            const distance =

                dispatch.distance !== null &&
                dispatch.distance !== undefined

                    ? `${dispatch.distance} km`

                    : "-";


            /* ---------------------------------------------
               ETA
               --------------------------------------------- */

            const eta =

                dispatch.estimated_time_minutes !== null &&
                dispatch.estimated_time_minutes !== undefined

                    ? `${dispatch.estimated_time_minutes} min`

                    : "-";


            /* ---------------------------------------------
               Return table row
               --------------------------------------------- */

            return `

                <tr>

                    <!-- ID -->

                    <td>
                        #${dispatch.id}
                    </td>


                    <!-- Emergency -->

                    <td>

                        <div class="dispatch-main">
                            ${emergencyText}
                        </div>

                        <div class="dispatch-sub">
                            ${emergencyDetails}
                        </div>

                        <div>
                            ${emergencySeverity}
                        </div>

                    </td>


                    <!-- Resource -->

                    <td>

                        <div class="dispatch-main">
                            ${resourceName}
                        </div>

                        <div class="dispatch-sub">
                            ${resourceType}
                        </div>

                    </td>


                    <!-- Route -->

                    <td class="route-cell">

                        ${routeHTML}

                    </td>


                    <!-- Distance -->

                    <td>
                        <strong>
                            ${distance}
                        </strong>
                    </td>


                    <!-- ETA -->

                    <td>
                        <strong>
                            ${eta}
                        </strong>
                    </td>


                    <!-- Status -->

                    <td>
                        ${createBadge(
                            dispatch.status
                        )}
                    </td>


                    <!-- Action -->

                    <td>
                        ${action}
                    </td>

                </tr>

            `;

        }).join("");
}


/* =========================================================
   LOAD PRIORITY QUEUE
   ========================================================= */

async function loadPriorityQueue() {

    const emergencies =
        await fetchData(
            "/priority/emergencies"
        );


    const table =
        document.getElementById(
            "priorityTable"
        );


    /* -----------------------------------------------------
       Priority values
       ----------------------------------------------------- */

    const priorityValues = {

        "CRITICAL": 1,

        "HIGH": 2,

        "MEDIUM": 3,

        "LOW": 4

    };


    /* -----------------------------------------------------
       Handle empty queue
       ----------------------------------------------------- */

    if (
        !emergencies ||
        emergencies.length === 0
    ) {

        table.innerHTML = `
            <tr>

                <td
                    colspan="8"
                    class="empty-message"
                >
                    Priority queue is empty.
                </td>

            </tr>
        `;

        return;
    }


    /* -----------------------------------------------------
       Display priority queue
       ----------------------------------------------------- */

    table.innerHTML =
        emergencies.map(
            (emergency, index) => {


                /* -----------------------------------------
                   Get priority number
                   ----------------------------------------- */

                const priority =
                    priorityValues[
                        String(
                            emergency.severity
                        ).toUpperCase()
                    ] || 4;


                /* -----------------------------------------
                   Location
                   ----------------------------------------- */

                const location =
                    locationsMap[
                        emergency.location_id
                    ]
                    ||
                    `Location #${emergency.location_id}`;


                /* -----------------------------------------
                   Reported time
                   ----------------------------------------- */

                const reported =
                    emergency.created_at

                        ? new Date(
                            emergency.created_at
                          ).toLocaleString()

                        : "N/A";


                /* -----------------------------------------
                   Priority class
                   ----------------------------------------- */

                let priorityClass =
                    "priority-low";


                if (priority === 1) {

                    priorityClass =
                        "priority-critical";

                } else if (priority === 2) {

                    priorityClass =
                        "priority-high";

                } else if (priority === 3) {

                    priorityClass =
                        "priority-medium";
                }


                /* -----------------------------------------
                   Return row
                   ----------------------------------------- */

                return `

                    <tr>

                        <!-- Position -->

                        <td>

                            <span
                                class="queue-position"
                            >
                                ${index + 1}
                            </span>

                        </td>


                        <!-- Priority -->

                        <td>

                            <span
                                class="
                                    priority-number
                                    ${priorityClass}
                                "
                            >
                                ${priority}
                            </span>

                        </td>


                        <!-- Emergency ID -->

                        <td>

                            <strong>
                                #${emergency.id}
                            </strong>

                        </td>


                        <!-- Type -->

                        <td>
                            ${emergency.type}
                        </td>


                        <!-- Severity -->

                        <td>

                            ${createBadge(
                                emergency.severity
                            )}

                        </td>


                        <!-- Status -->

                        <td>

                            ${createBadge(
                                emergency.status
                            )}

                        </td>


                        <!-- Location -->

                        <td>
                            ${location}
                        </td>


                        <!-- Reported -->

                        <td>
                            ${reported}
                        </td>

                    </tr>

                `;

            }
        ).join("");
}

/* =========================================================
   SYSTEM ANALYTICS
   ========================================================= */

async function loadAnalytics() {

    try {

        const emergencies =
            await fetchData("/emergencies/");

        const resources =
            await fetchData("/resources/");


        /* -------------------------------------------------
           EMERGENCY SEVERITY COUNTS
           ------------------------------------------------- */

        const critical =
            emergencies.filter(
                emergency =>
                    emergency.severity === "CRITICAL"
            ).length;


        const high =
            emergencies.filter(
                emergency =>
                    emergency.severity === "HIGH"
            ).length;


        const medium =
            emergencies.filter(
                emergency =>
                    emergency.severity === "MEDIUM"
            ).length;


        const low =
            emergencies.filter(
                emergency =>
                    emergency.severity === "LOW"
            ).length;


        const totalEmergencies =
            emergencies.length;


        /* -------------------------------------------------
           Update counts
           ------------------------------------------------- */

        document.getElementById(
            "criticalCount"
        ).textContent = critical;


        document.getElementById(
            "highCount"
        ).textContent = high;


        document.getElementById(
            "mediumCount"
        ).textContent = medium;


        document.getElementById(
            "lowCount"
        ).textContent = low;


        /* -------------------------------------------------
           Calculate bar widths
           ------------------------------------------------- */

        const criticalWidth =
            totalEmergencies > 0
                ? (critical / totalEmergencies) * 100
                : 0;


        const highWidth =
            totalEmergencies > 0
                ? (high / totalEmergencies) * 100
                : 0;


        const mediumWidth =
            totalEmergencies > 0
                ? (medium / totalEmergencies) * 100
                : 0;


        const lowWidth =
            totalEmergencies > 0
                ? (low / totalEmergencies) * 100
                : 0;


        document.getElementById(
            "criticalBar"
        ).style.width = `${criticalWidth}%`;


        document.getElementById(
            "highBar"
        ).style.width = `${highWidth}%`;


        document.getElementById(
            "mediumBar"
        ).style.width = `${mediumWidth}%`;


        document.getElementById(
            "lowBar"
        ).style.width = `${lowWidth}%`;


        /* -------------------------------------------------
           RESOURCE COUNTS
           ------------------------------------------------- */

        const totalResources =
            resources.length;


        const available =
            resources.filter(
                resource =>
                    resource.status === "AVAILABLE"
            ).length;


        const dispatched =
            resources.filter(
                resource =>
                    resource.status === "DISPATCHED"
            ).length;


        const busy =
            resources.filter(
                resource =>
                    resource.status === "BUSY"
            ).length;


        const activeResources =
            dispatched + busy;


        /* -------------------------------------------------
           Update resource numbers
           ------------------------------------------------- */

        document.getElementById(
            "analyticsAvailable"
        ).textContent =
            `${available} / ${totalResources}`;


        document.getElementById(
            "analyticsDispatched"
        ).textContent =
            `${dispatched} / ${totalResources}`;


        document.getElementById(
            "analyticsBusy"
        ).textContent =
            `${busy} / ${totalResources}`;


        document.getElementById(
            "analyticsTotalResources"
        ).textContent =
            totalResources;


        document.getElementById(
            "analyticsActiveResources"
        ).textContent =
            activeResources;


        /* -------------------------------------------------
           Resource progress bars
           ------------------------------------------------- */

        const availableWidth =
            totalResources > 0
                ? (available / totalResources) * 100
                : 0;


        const dispatchedWidth =
            totalResources > 0
                ? (dispatched / totalResources) * 100
                : 0;


        const busyWidth =
            totalResources > 0
                ? (busy / totalResources) * 100
                : 0;


        document.getElementById(
            "availableResourceBar"
        ).style.width =
            `${availableWidth}%`;


        document.getElementById(
            "dispatchedResourceBar"
        ).style.width =
            `${dispatchedWidth}%`;


        document.getElementById(
            "busyResourceBar"
        ).style.width =
            `${busyWidth}%`;


    } catch (error) {

        console.error(
            "Analytics loading error:",
            error
        );

    }
}

/* =========================================================
   LOAD ENTIRE DASHBOARD
   ========================================================= */

async function loadDashboard() {

    try {

        /*
         * Load locations FIRST.
         *
         * Other sections depend on locationsMap.
         */

        await loadLocations();

        /*
         * Load location dropdown.
         */

        await loadEmergencyLocations();


        /*
         * Load all dashboard sections.
         */

        await Promise.all([
    loadEmergencies(),
    loadResources(),
    loadDispatches(),
    loadPriorityQueue(),
    loadAnalytics()
]);


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );
    }
}


/* =========================================================
   START DASHBOARD
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "Smart Emergency Response Dashboard loaded."
        );

        loadDashboard();

    }
);