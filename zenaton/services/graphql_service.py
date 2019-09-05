from ..exceptions import InternalError
import json
import requests


class GraphQLService:

    # Queries
    FIND_WORKFLOW = """
        query ($custom_id: String!, $environment_name: String!, $programming_language: ProgrammingLanguage!, $name: String!) {
            findWorkflow(custom_id: $custom_id, environment_name: $environment_name, programming_language: $programming_language, name: $name) {
                id
                name
                properties
            }
        }
    """

    # Mutations
    CREATE_WORKFLOW_SCHEDULE = """
        mutation ($input: CreateWorkflowScheduleInput!) {
            createWorkflowSchedule(input: $input) {
                schedule {
                    id
                    name
                    cron
                    insertedAt
                    updatedAt
                    target {
                        ... on WorkflowTarget {
                            name
                            type
                            canonicalName
                            programmingLanguage
                            properties
                        }
                    }
                }
            }
        }
    """

    CREATE_TASK_SCHEDULE = """
        mutation ($input: CreateTaskScheduleInput!) {
            createTaskSchedule(input: $input) {
                schedule {
                    id
                    name
                    cron
                    insertedAt
                    updatedAt
                    target {
                        ... on TaskTarget {
                            name
                            type
                            programmingLanguage
                            properties
                        }
                    }
                }
            }
        }
    """

    DISPATCH_TASK = """
        mutation dispatchTask($input: DispatchTaskInput!) {
            dispatchTask(input: $input) {
                task {
                    intentId
                }
            }
        }
    """

    DISPATCH_WORKFLOW = """
        mutation dispatchWorkflow($input: DispatchWorkflowInput!) {
            dispatchWorkflow(input: $input) {
                workflow {
                    id
                }
            }
        }
    """

    KILL_WORKFLOW = """
        mutation killWorkflow($input: KillWorkflowInput!) {
            killWorkflow(input: $input) {
                id
            }
        }
    """

    PAUSE_WORKFLOW = """
        mutation pauseWorkflow($input: PauseWorkflowInput!) {
            pauseWorkflow(input: $input) {
                id
            }
        }
    """

    RESUME_WORKFLOW = """
        mutation resumeWorkflow($input: ResumeWorkflowInput!) {
            resumeWorkflow(input: $input) {
                id
            }
        }
    """

    SEND_EVENT = """
        mutation sendEventToWorkflowByNameAndCustomId($input: SendEventToWorkflowByNameAndCustomIdInput!) {
            sendEventToWorkflowByNameAndCustomId(input: $input) {
                event {
                    intentId
                }
            }
        }
    """

    def request(self, url, query, variables=None, headers={}):
        try:
            data = {'query': query}
            if variables:
                data['variables'] = variables
            r = requests.request(method='POST', url=url,
                                 headers=headers, data=json.dumps(data))
            if r.status_code >= 400:
                raise InternalError(r.content)
            content = r.json()

        except json.decoder.JSONDecodeError:
            raise InternalError
        except requests.exceptions.ConnectionError:
            raise ConnectionError
        return content
