<script>
    import {Github, FileTypeCorner, CirclePlay} from 'lucide-svelte';

    let prompt = "";
    let f_stack_options = [
        {
            id: 1,
            text: `Angular`
        },
        {
            id: 2,
            text: `React`
        },
        {
            id: 3,
            text: `Svelte`
        },
        {
            id: 4,
            text: `Vue`
        }
    ];
    let b_stack_options = [
        {
            id: 1,
            text: `Golang`
        },
        {
            id: 2,
            text: `Python`
        },
        {
            id: 3,
            text: `PHP`
        },
        {
            id: 4,
            text: `Node.js`
        }
    ];

</script>

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

        <div class="w-full bg-[#16171a] border border-white/10 rounded-2xl p-4 shadow-2xl focus-within:border-white/20 transition-all">
      <textarea
              bind:value={prompt}
              placeholder="Describe your project idea here..."
              class="w-full bg-transparent border-none focus:outline-0 text-lg resize-none min-h-[100px] placeholder:text-gray-600"
      ></textarea>

            <div class="flex items-center justify-end mt-4">
                <button class="p-2 bg-stormy-teal hover:bg-yale-blue cursor-pointer flex items-center gap-2 rounded-lg transition-all shadow-[0_0_15px_rgba(147,51,234,0.3)]">
                    <CirclePlay size={18}/>
                </button>
            </div>
        </div>

        <div class="w-full mt-4 flex flex-wrap items-center justify-between gap-3">
            <div class="flex gap-3 flex-1">
                <select class="flex-1 cursor-pointer md:flex-none flex items-center justify-between px-2 py-1 bg-[#16171a]/50 border border-white/5 rounded-xl text-sm text-white transition-all">
                    <option value="">Preferred front-end stack</option>
                    {#each f_stack_options as option}
                        <option value={option}>
                            {option.text}
                        </option>
                    {/each}
                </select>
                <select class="flex-1 cursor-pointer md:flex-none flex items-center justify-between px-2 py-1 bg-[#16171a]/50 border border-white/5 rounded-xl text-sm text-white transition-all">
                    <option value="">Preferred back-end stack</option>
                    {#each b_stack_options as option}
                        <option value={option}>
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

    </div>
</main>

<style>
    textarea::-webkit-scrollbar {
        width: 0px;
    }
</style>