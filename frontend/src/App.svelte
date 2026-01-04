<script lang="ts">
    import {CirclePlay, Github, Loader} from 'lucide-svelte';
    import {b_stack_options, f_stack_options} from "./stack_options.ts";
    import type {ProjectPlan} from "./types/ProjectPlan.ts";
    import type {ProjectTask} from "./types/ProjectTask.ts";
    import type {ExplanationTab} from "./types/ExplanationTab.ts";
    import {onMount} from "svelte";
    import {loadFromDB, saveToDB} from "./indexedDB/indexedDB.ts";
    import TasksList from "./TasksList.svelte";
    import ExplanationSidebar from "./ExplanationSidebar.svelte";


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
    let isDataLoaded = false; // Flag to prevent saving during initial load

    onMount(async () => {
    try {
        const data = await loadFromDB();

        if (data.projectPlan) projectPlan = data.projectPlan;
        if (data.frontStack !== undefined) frontStack = data.frontStack;
        if (data.backStack !== undefined) backStack = data.backStack;
        if (data.idea !== undefined) idea = data.idea;

        if (data.tabs?.length) {
            tabs = data.tabs;
            activeTabId = data.tabs[0].id;
            isSidebarOpen = true;
        }

        isDataLoaded = true; // Mark data as loaded, now we can save changes

    } catch (error) {
        console.error("Error loading data:", error);
        isDataLoaded = true; // Even on error, allow saving
    }
});

    // Reactive Savers - only save after initial data load
    $: if (isDataLoaded && projectPlan) saveToDB("projectPlan", projectPlan);
    $: if (isDataLoaded && tabs) saveToDB("tabs", tabs);
    $: if (isDataLoaded && frontStack !== undefined) saveToDB("frontStack", frontStack);
    $: if (isDataLoaded && backStack !== undefined) saveToDB("backStack", backStack);
    $: if (isDataLoaded && idea !== undefined) saveToDB("idea", idea);

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
            const errorMessage = e instanceof Error ? e.message : String(e);
            alert("Error generating plan: " + errorMessage);
        } finally {
            loading = false;
        }
    }

    async function openTaskTab(task: ProjectTask) {

        if (!projectPlan) {
            alert("Please generate a project plan first");
            return
        };

        isSidebarOpen = true;

        const existingTab = tabs.find(t => t.id === task.title);
        if (existingTab) {
            if (existingTab.data !== null) {
                activeTabId = existingTab.id;
                return;
            }
            activeTabId = existingTab.id;
        } else {
            const newTab = {
                id: task.title,
                title: task.title,
                description: task.description,
                data: null,
                loading: true
            };
            tabs = [...tabs, newTab];
            activeTabId = newTab.id;
        }

        tabs = tabs.map(t => t.id === task.title ? {...t, loading: true} : t);

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
            tabs = tabs.filter(t => t.id !== task.title);
            alert("Failed to explain task");
        }
    }


</script>

<main class="relative min-h-screen w-full bg-[#0a0a0b] text-white flex flex-col items-center justify-center px-4 overflow-hidden font-sans">

    <div class="absolute inset-0 z-0"
         id="bg-grid-pattern">
        <div class="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_20%_50%,rgba(50,100,255,0.05),transparent_25%)]"></div>
        <div class="absolute top-0 right-0 w-full h-full bg-[radial-gradient(circle_at_80%_50%,rgba(255,100,50,0.05),transparent_25%)]"></div>
    </div>
    <div class="flex justify-between sticky w-full h-20 items-center">
        <div class="flex items-center gap-2 px-4 py-2 md:px-8 md:py-4">
            <img src="/logo_full.svg" alt="Side Project Starter Pack Logo" class="h-8" />
            <h1 class="text-2xl md:text-3xl text-stormy-teal font-bold tracking-tight ">Side Project Starter Pack</h1>
        </div>
        <div>
            <a href="https://github.com/deslancer/Side-Project-Starter-Pack/tree/main" target="_blank" class="text-gray-500 hover:text-white transition-colors">
                <Github size={28}/>
            </a>
        </div>
    </div>
    <div class="relative z-10 w-full max-w-3xl flex flex-col items-center text-center">
        <h2 class="text-3xl md:text-4xl font-semibold tracking-tight mb-4">
            <span class="text-alabaster-grey">Prompt it,</span> <span class="text-stormy-teal">discover it,</span> <span
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
                        class="p-2 bg-stormy-teal hover:bg-yale-blue cursor-pointer
                         disabled:cursor-not-allowed
                         disabled:hover:bg-stormy-teal
                         flex items-center gap-2 rounded-lg
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

        </div>
        <div class="border-b border-b-graphite h-1 w-full my-5"></div>
        {#if projectPlan}
            <TasksList projectPlan={projectPlan} tabs={tabs} openTaskTab={openTaskTab}/>
        {/if}
    </div>
    <ExplanationSidebar bind:isOpen={isSidebarOpen} bind:tabs={tabs} bind:activeTabId={activeTabId}/>
</main>

<style>
    textarea::-webkit-scrollbar {
        width: 0px;
    }
</style>