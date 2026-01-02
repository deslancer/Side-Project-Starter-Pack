// --- INDEXED DB HELPER ---
const DB_NAME = "DevStepDB";
const STORE_NAME = "session";

const dbRequest = window.indexedDB.open(DB_NAME, 1);

dbRequest.onupgradeneeded = (e:IDBVersionChangeEvent) => {
    if (!e.oldVersion) return;
    const db = (e.target as IDBRequest).result;
    if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME);
    }
};

function saveToDB(key: string, value: any) {
    const dbReq = window.indexedDB.open(DB_NAME, 1);
    dbReq.onsuccess = (e: Event) => {
        const db = (e.target as IDBRequest).result;
        const tx = db.transaction(STORE_NAME, "readwrite");
        tx.objectStore(STORE_NAME).put(value, key);
    };
}

function loadProjectPlan(): Promise<any> {
    return new Promise((resolve) => {
        const dbReq = window.indexedDB.open(DB_NAME, 1);
        dbReq.onsuccess = (e: Event) => {
            const db = (e.target as IDBRequest).result;
            const tx = db.transaction(STORE_NAME, "readonly");
            const store = tx.objectStore(STORE_NAME);
            const reqPlan = store.get("projectPlan");

            reqPlan.onsuccess = () => {
                resolve(reqPlan.result || null);
            };
            reqPlan.onerror = () => {
                resolve(null);
            };
        };
        dbReq.onerror = () => {
            resolve(null);
        };
    });
}

function loadTabs(): Promise<any[]> {
    return new Promise((resolve) => {
        const dbReq = window.indexedDB.open(DB_NAME, 1);
        dbReq.onsuccess = (e: Event) => {
            const db = (e.target as IDBRequest).result;
            const tx = db.transaction(STORE_NAME, "readonly");
            const store = tx.objectStore(STORE_NAME);
            const reqTabs = store.get("tabs");

            reqTabs.onsuccess = () => {
                resolve(reqTabs.result || []);
            };
            reqTabs.onerror = () => {
                resolve([]);
            };
        };
        dbReq.onerror = () => {
            resolve([]);
        };
    });
}

async function loadFromDB() {
    const [projectPlan, tabs] = await Promise.all([
        loadProjectPlan(),
        loadTabs()
    ]);
    
    return {
        projectPlan,
        tabs
    };
}

export { saveToDB, loadFromDB, loadProjectPlan, loadTabs };