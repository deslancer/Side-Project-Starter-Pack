import type {ProjectTask} from "./ProjectTask.ts";

export interface ProjectPlan {
    project_name: string
    suggested_stack: string[]
    tasks: ProjectTask[]
    status?: string
}