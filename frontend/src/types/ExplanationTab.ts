import type {ExplanationTask} from "./ExplanationTask.ts";

export interface ExplanationTab {
    id: string
    title: string
    data: ExplanationTask | null
    loading: boolean
}