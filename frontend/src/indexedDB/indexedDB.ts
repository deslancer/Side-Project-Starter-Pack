// --- INDEXED DB HELPER ---
const DB_NAME = "DevStepDB";
const STORE_NAME = "session";
const DB_VERSION = 2; // Incremented to force upgrade for existing databases

function openDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
        const dbReq = window.indexedDB.open(DB_NAME, DB_VERSION);
        
        dbReq.onupgradeneeded = (e: IDBVersionChangeEvent) => {
            const db = (e.target as IDBRequest).result;
            // Create the object store if it doesn't exist
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                db.createObjectStore(STORE_NAME);
            }
        };
        
        dbReq.onsuccess = (e: Event) => {
            const db = (e.target as IDBRequest).result;
            // Verify the store exists before resolving
            if (db.objectStoreNames.contains(STORE_NAME)) {
                resolve(db);
            } else {
                // This shouldn't happen, but if it does, reject
                db.close();
                reject(new Error(`Object store "${STORE_NAME}" was not created`));
            }
        };
        
        dbReq.onerror = () => {
            reject(dbReq.error);
        };
    });
}

function saveToDB(key: string, value: any) {
    openDB().then((db) => {
        const tx = db.transaction(STORE_NAME, "readwrite");
        tx.objectStore(STORE_NAME).put(value, key);
    }).catch((error) => {
        console.error("Error saving to IndexedDB:", error);
    });
}

function loadProjectPlan(): Promise<any> {
    return new Promise((resolve) => {
        openDB().then((db) => {
            const tx = db.transaction(STORE_NAME, "readonly");
            const store = tx.objectStore(STORE_NAME);
            const reqPlan = store.get("projectPlan");

            reqPlan.onsuccess = () => {
                resolve(reqPlan.result || null);
            };
            reqPlan.onerror = () => {
                resolve(null);
            };
        }).catch(() => {
            resolve(null);
        });
    });
}

function loadTabs(): Promise<any[]> {
    return new Promise((resolve) => {
        openDB().then((db) => {
            const tx = db.transaction(STORE_NAME, "readonly");
            const store = tx.objectStore(STORE_NAME);
            const reqTabs = store.get("tabs");

            reqTabs.onsuccess = () => {
                resolve(reqTabs.result || []);
            };
            reqTabs.onerror = () => {
                resolve([]);
            };
        }).catch(() => {
            resolve([]);
        });
    });
}

function loadFormData(): Promise<{frontStack: string, backStack: string, idea: string}> {
    return new Promise((resolve) => {
        openDB().then((db) => {
            const tx = db.transaction(STORE_NAME, "readonly");
            const store = tx.objectStore(STORE_NAME);
            
            const reqFrontStack = store.get("frontStack");
            const reqBackStack = store.get("backStack");
            const reqIdea = store.get("idea");
            
            let frontStack = "";
            let backStack = "";
            let idea = "";
            let completed = 0;
            
            const checkComplete = () => {
                completed++;
                if (completed === 3) {
                    resolve({ frontStack, backStack, idea });
                }
            };
            
            reqFrontStack.onsuccess = () => {
                frontStack = reqFrontStack.result || "";
                checkComplete();
            };
            reqFrontStack.onerror = () => checkComplete();
            
            reqBackStack.onsuccess = () => {
                backStack = reqBackStack.result || "";
                checkComplete();
            };
            reqBackStack.onerror = () => checkComplete();
            
            reqIdea.onsuccess = () => {
                idea = reqIdea.result || "";
                checkComplete();
            };
            reqIdea.onerror = () => checkComplete();
        }).catch(() => {
            resolve({ frontStack: "", backStack: "", idea: "" });
        });
    });
}

async function loadFromDB() {
    const [projectPlan, tabs, formData] = await Promise.all([
        loadProjectPlan(),
        loadTabs(),
        loadFormData()
    ]);
    
    return {
        projectPlan,
        tabs,
        ...formData
    };
}

export { saveToDB, loadFromDB, loadProjectPlan, loadTabs, loadFormData };