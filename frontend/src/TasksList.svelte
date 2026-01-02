<script lang="ts">
    import type {ProjectPlan} from "./types/ProjectPlan.ts";
    import type {ProjectTask} from "./types/ProjectTask.ts";

    export let projectPlan: ProjectPlan;
    export let openTaskTab: (task: ProjectTask) => void;
</script>

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