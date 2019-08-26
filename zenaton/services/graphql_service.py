from ..exceptions import ExternalError, InternalError
import json
import requests


class GraphQLService:
    CREATE_WORKFLOW_SCHEDULE = """
        mutation ($createWorkflowScheduleInput: CreateWorkflowScheduleInput!) {
            createWorkflowSchedule(input: $createWorkflowScheduleInput) {
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
        mutation ($createTaskScheduleInput: CreateTaskScheduleInput!) {
            createTaskSchedule(input: $createTaskScheduleInput) {
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
            content['status_code'] = r.status_code

            if 'errors' in content and isinstance(content['errors'], list) and len(content['errors']) > 0:
                errors = content['errors']
                for error in errors:
                    if 'locations' in error:
                        del error['locations']
                raise ExternalError(errors)
        except json.decoder.JSONDecodeError:
            raise InternalError
        except requests.exceptions.ConnectionError:
            raise ConnectionError
        return content
