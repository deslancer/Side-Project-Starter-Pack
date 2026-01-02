<script lang="ts">
    import atom_one_dark_reasonable from "svelte-highlight/styles/atom-one-dark-reasonable";
    import {HighlightAuto} from "svelte-highlight";
    import type {ExplanationTab} from "./types/ExplanationTab.ts";
    export let tabs: ExplanationTab[] = [];
    export let activeTabId: string | null = null;
    export let isOpen = false;

    function closeTab(e: MouseEvent | KeyboardEvent, id: string) {
        e.stopPropagation();
        tabs = tabs.filter(t => t.id !== id);
        if (activeTabId === id) {
            activeTabId = tabs.length ? tabs[0].id : null;
        }
        if (tabs.length === 0) isOpen = false;
    }
</script>
<svelte:head>
    {@html atom_one_dark_reasonable}
</svelte:head>
<div class="fixed right-0 top-0 h-full bg-white shadow-2xl border-l border-gray-200 transform transition-transform duration-300 z-50 flex flex-col w-[400px] xl:w-[600px] {isOpen ? 'translate-x-0' : 'translate-x-full'}">

    {#if isOpen}
        <button
                on:click={() => isOpen = false}
                class="absolute cursor-pointer -left-10 top-4 bg-white p-2 rounded-l-lg shadow-md border border-r-0 border-gray-200 text-gray-500 hover:text-red-500"
        >
            ✕
        </button>
    {/if}

    <div class="flex bg-gray-100 border-b border-gray-200 overflow-x-auto no-scrollbar">
        {#each tabs as tab}
            <div
                    role="button"
                    tabindex="0"
                    on:click={() => activeTabId = tab.id}
                    on:keydown={(e) => e.key === 'Enter' || e.key === ' ' ? activeTabId = tab.id : null}
                    class="flex items-center gap-2 px-4 py-3 text-sm font-medium cursor-pointer border-r border-gray-200 min-w-[120px] max-w-[200px] truncate select-none transition-colors
            {activeTabId === tab.id ? 'bg-white text-yale-blue border-b-2 border-b-stormy-teal' : 'bg-gray-50 text-gray-500 hover:bg-gray-100'}"
            >
                <span class="truncate">{tab.title}</span>
                <span
                        role="button"
                        tabindex="0"
                        on:click={(e) => closeTab(e, tab.id)}
                        on:keydown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                                e.preventDefault();
                                closeTab(e, tab.id);
                            }
                        }}
                        class="text-gray-400 hover:text-red-500 rounded-full p-1 hover:bg-gray-200"
                >
              ×
            </span>
            </div>
        {/each}
    </div>

    <div class="flex-1 overflow-y-auto p-6 bg-gray-50">
        {#if tabs.length === 0}
            <div class="h-full flex flex-col items-center justify-center text-gray-400">
                <svg class="w-16 h-16 mb-4 opacity-20" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                    <path fill-rule="evenodd"
                          d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                          clip-rule="evenodd"/>
                </svg>
                <p>Select a task to see details</p>
            </div>
        {:else}
            {#each tabs as tab}
                {#if activeTabId === tab.id}
                    <div class="animate-fade-in">
                        {#if tab.loading}
                            <div class="flex flex-col items-center justify-center py-20">
                                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-yale-blue"></div>
                                <p class="mt-4 text-gray-500">Asking Mentor...</p>
                            </div>
                        {:else if tab.data}
                            <div class="prose max-w-none">
                                <h3 class="text-xl font-bold text-gray-800 mb-2">{tab.title}</h3>
                                <p class="text-gray-600 mb-6">{tab.data.explanation}</p>

                                <div class="relative group">
                                    <div class="absolute right-2 top-2 text-xs text-gray-500 font-mono">bash /
                                        code
                                    </div>
                                    <HighlightAuto code={tab.data.code_snippet} />
                                </div>

                                <div class="mt-6">
                                    <h4 class="text-sm font-bold text-gray-500 uppercase tracking-wide mb-3">Learn
                                        More</h4>
                                    <div class="flex flex-wrap gap-2">
                                        {#each tab.data.related_docs as doc}
                                            <a
                                                    href="https://www.google.com/search?q={doc}"
                                                    target="_blank"
                                                    class="px-3 py-1 bg-white border border-gray-300 text-gray-600 text-sm rounded-full hover:border-blue-500 hover:text-blue-500 transition flex items-center gap-1"
                                            >
                                                {doc} ↗
                                            </a>
                                        {/each}
                                    </div>
                                </div>
                            </div>
                        {/if}
                    </div>
                {/if}
            {/each}
        {/if}
    </div>
</div>