<script lang="ts">
    import {CirclePlay, FileTypeCorner, Github, Loader} from 'lucide-svelte';
    import {b_stack_options, f_stack_options} from "./stack_options.ts";
    import type {ProjectPlan} from "./types/ProjectPlan.ts";
    import type {ProjectTask} from "./types/ProjectTask.ts";
    import type {ExplanationTab} from "./types/ExplanationTab.ts";
    import {onMount} from "svelte";
    import {loadFromDB, saveToDB} from "./indexedDB/indexedDB.ts";
    import { HighlightAuto } from "svelte-highlight";
    import atom_one_dark_reasonable from "svelte-highlight/styles/atom-one-dark-reasonable";

    let idea = "";
    let frontStack = ""
    let backStack = ""
    let techStack: string;
    $: techStack = (frontStack && backStack)
        ? `${frontStack}+${backStack}`
        : "AI decides";
    let loading = false;
    let projectPlan: ProjectPlan | null = null;

    // Sidebar State
    let isSidebarOpen = false;
    let tabs: ExplanationTab[] = [];
    let activeTabId: string | null = null;

    onMount(async () => {
        const {projectPlan: loadedPlan, tabs: loadedTabs} = await loadFromDB();

        if (loadedPlan) {
            projectPlan = loadedPlan;
        }

        if (loadedTabs && loadedTabs.length > 0) {
            tabs = loadedTabs;
            activeTabId = loadedTabs[0].id;
            isSidebarOpen = true;
        }
    });

    // Reactive Savers
    $: if (projectPlan) saveToDB("projectPlan", projectPlan);
    $: if (tabs) saveToDB("tabs", tabs);

    async function generatePlan(): Promise<ProjectPlan | null | undefined> {
        if (!idea) {
            alert("Please enter an idea");
            return null

        }
        loading = true;
        projectPlan = null;

        try {
            const res = await fetch("http://127.0.0.1:8000/api/generate", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({prompt: idea, tech_stack: techStack}),
            });

            const data = await res.json();
            if (data.status === "success") {
                projectPlan = data.result;
            }
        } catch (e) {
            alert("Error generating plan: " + e.message);
        } finally {
            loading = false;
        }
    }

    async function openTaskTab(task: ProjectTask) {

        if (!projectPlan) {
            alert("Please generate a project plan first");
            return
        }
        ;

        isSidebarOpen = true;

        const existingTab = tabs.find(t => t.id === task.title);
        if (existingTab) {
            activeTabId = existingTab.id;
            return;
        }

        const newTab = {
            id: task.title,
            title: task.title,
            description: task.description,
            data: null,
            loading: true
        };

        tabs = [...tabs, newTab];
        activeTabId = newTab.id;

        // 3. Делаем запрос
        try {
            const res = await fetch("http://127.0.0.1:8000/api/explain", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    task_title: task.title,
                    task_description: task.description,
                    tech_stack: projectPlan.suggested_stack.join(", "),
                    project_context: projectPlan.project_name
                }),
            });
            const result = await res.json();

            tabs = tabs.map(t => t.id === task.title ? {...t, data: result, loading: false} : t);

        } catch (e) {
            console.error(e);
            // Удаляем таб если ошибка (или показываем ошибку внутри)
            tabs = tabs.filter(t => t.id !== task.title);
            alert("Failed to explain task");
        }
    }

    function closeTab(e: MouseEvent, id: string) {
        e.stopPropagation();
        tabs = tabs.filter(t => t.id !== id);
        if (activeTabId === id) {
            activeTabId = tabs.length ? tabs[0].id : null;
        }
        if (tabs.length === 0) isSidebarOpen = false;
    }

</script>
<svelte:head>
    {@html atom_one_dark_reasonable}
</svelte:head>
<main class="relative min-h-screen w-full bg-[#0a0a0b] text-white flex flex-col items-center justify-center px-4 overflow-hidden font-sans">

    <div class="absolute inset-0 z-0"
         id="bg-grid-pattern">
        <div class="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_20%_50%,rgba(50,100,255,0.05),transparent_25%)]"></div>
        <div class="absolute top-0 right-0 w-full h-full bg-[radial-gradient(circle_at_80%_50%,rgba(255,100,50,0.05),transparent_25%)]"></div>
    </div>

    <div class="relative z-10 w-full max-w-3xl flex flex-col items-center text-center">
        <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">Side Project Starter Pack</h1>
        <h2 class="text-3xl md:text-4xl font-semibold tracking-tight mb-4">
            <span class="text-alabaster-grey">Prompt it,</span> <span class="text-stormy-teal">tweak it,</span> <span
                class="text-yale-blue">use it</span>
        </h2>

        <p class="text-gray-400 text-lg mb-10 max-w-lg">
            Your <span class="text-stormy-teal">AI Dev Adviser</span>, build dev stack roadmap from your idea!
        </p>

        <div class="w-full bg-[#16171a] border border-white/10 rounded-2xl p-4 shadow-2xl focus-within:border-white/20
         transition-all">
      <textarea
              bind:value={idea}
              placeholder="Describe your project idea here..."
              class="w-full bg-transparent border-none focus:outline-0 text-lg resize-none min-h-[100px] placeholder:text-gray-600"
      ></textarea>

            <div class="flex items-center justify-end mt-4">
                <button
                        on:click={generatePlan}
                        disabled={loading}
                        class="p-2 bg-stormy-teal hover:bg-yale-blue cursor-pointer flex items-center gap-2 rounded-lg
                         transition-all shadow-[0_0_15px_rgba(147,51,234,0.3)]">
                    {#if loading}
                        <span>Thinking...</span>
                        <Loader size={18} class="animate-spin"/>
                    {:else}
                        <span>Generate</span>
                        <CirclePlay size={18}/>
                    {/if}
                </button>
            </div>
        </div>

        <div class="w-full mt-4 flex flex-wrap items-center justify-between gap-3">
            <div class="flex gap-3 flex-1">
                <select bind:value={frontStack}
                        class="flex-1 cursor-pointer md:flex-none flex items-center justify-between px-2 py-1 bg-[#16171a]/50 border border-white/5 rounded-xl text-sm text-white transition-all">
                    <option value="">Preferred front-end stack</option>
                    {#each f_stack_options as option}
                        <option value={option.text}>
                            {option.text}
                        </option>
                    {/each}
                </select>
                <select
                        bind:value={backStack}
                        class="flex-1 cursor-pointer md:flex-none flex items-center justify-between px-2 py-1 bg-[#16171a]/50 border border-white/5 rounded-xl text-sm text-white transition-all">
                    <option value="">Preferred back-end stack</option>
                    {#each b_stack_options as option}
                        <option value={option.text}>
                            {option.text}
                        </option>
                    {/each}
                </select>
            </div>

            <div class="flex items-center gap-2">
                <a href="#" class="text-gray-500 hover:text-white transition-colors">
                    <FileTypeCorner size={20}/>
                </a>

                <div class="flex items-center gap-3 ml-2 border-l border-white/10 pl-4">
                    <a href="#" class="text-gray-500 hover:text-white transition-colors">
                        <Github size={20}/>
                    </a>
                </div>
            </div>
        </div>
        <div class="border-b border-b-graphite h-1 w-full my-5"></div>
        {#if projectPlan}
            <div class="animate-fade-in-up mt-10">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">{projectPlan.project_name}</h2>
                    <div class="flex gap-2 flex-wrap justify-end">
                        {#each projectPlan.suggested_stack as tech}
              <span class="px-3 py-1 bg-yale-blue text-alabaster-grey text-xs font-semibold rounded-full">
                {tech}
              </span>
                        {/each}
                    </div>
                </div>

                <div class="relative border-l-2 border-stormy-teal ml-4 space-y-8">
                    {#each projectPlan.tasks as task, i}
                        <div class="relative pl-8">
                            <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-yale-blue border-4 border-alabaster-grey shadow-sm"></div>

                            <div class="bg-white p-5 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition group">
                                <div class="flex justify-between items-start">
                                    <div class="text-left">
                                        <h3 class="text-lg font-bold text-gray-800">Step {i + 1}: {task.title}</h3>
                                        <p class="text-gray-600 mt-1">{task.description}</p>
                                        <p class="text-xs text-gray-400 mt-2 font-mono">💡
                                            Hint: {task.technical_hint}</p>
                                    </div>

                                    <button
                                            on:click={() => openTaskTab(task)}
                                            class="ml-4 p-2 text-yale-blue hover:bg-blue-50 rounded-full transition tooltip cursor-pointer"
                                            title="How do I do this?"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                             viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                             stroke-linecap="round" stroke-linejoin="round">
                                            <circle cx="12" cy="12" r="10"/>
                                            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                                            <path d="M12 17h.01"/>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
    <div class="fixed right-0 top-0 h-full bg-white shadow-2xl border-l border-gray-200 transform transition-transform duration-300 z-50 flex flex-col w-[400px] xl:w-[600px] {isSidebarOpen ? 'translate-x-0' : 'translate-x-full'}">

        <button
                on:click={() => isSidebarOpen = false}
                class="absolute -left-10 top-4 bg-white p-2 rounded-l-lg shadow-md border border-r-0 border-gray-200 text-gray-500 hover:text-red-500"
        >
            ✕
        </button>

        <div class="flex bg-gray-100 border-b border-gray-200 overflow-x-auto no-scrollbar">
            {#each tabs as tab}
                <div
                        on:click={() => activeTabId = tab.id}
                        class="flex items-center gap-2 px-4 py-3 text-sm font-medium cursor-pointer border-r border-gray-200 min-w-[120px] max-w-[200px] truncate select-none transition-colors
            {activeTabId === tab.id ? 'bg-white text-blue-600 border-t-2 border-t-blue-600' : 'bg-gray-50 text-gray-500 hover:bg-gray-100'}"
                >
                    <span class="truncate">{tab.title}</span>
                    <span
                            on:click={(e) => closeTab(e, tab.id)}
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
                                        <div class="absolute right-2 top-2 text-xs text-gray-500 font-mono">BASH /
                                            CODE
                                        </div>
                                        <HighlightAuto code={tab.data.code_snippet} />
                                        <!--<pre class="bg-[#1e1e1e] text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono shadow-inner border border-gray-700">{tab.data.code_snippet}</pre>-->
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
</main>

<style>
    textarea::-webkit-scrollbar {
        width: 0px;
    }
</style>