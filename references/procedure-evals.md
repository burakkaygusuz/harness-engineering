# Procedure: evals

## Part F. Add the skill evals

Do steps 1 to 5 for each skill.

1. Write the file `skills/<skill-name>/evals/evals.json`. Start with two or three test cases. Use this model:

   ```json
   {
     "skill_name": "<skill-name>",
     "evals": [
       {
         "id": 1,
         "prompt": "<A realistic request, as a user writes it.>",
         "expected_output": "<A short description of a good answer.>",
         "files": ["evals/files/<input-file>"],
         "assertions": [
           "<A statement that is true or false for the output>",
           "<Another statement that is true or false for the output>"
         ]
       },
       {
         "id": 2,
         "prompt": "<A second request. Make it different from the first request.>",
         "expected_output": "<A short description of a good answer.>",
         "files": ["evals/files/<other-input-file>"]
       }
     ]
   }
   ```

2. Add more assertions after you read the first outputs. Add each failure that you find to the `## Gotchas` section of the skill.
3. Write the file `skills/<skill-name>/evals/train_queries.json`. Include queries that must start the skill and queries that must not start it.
4. Add near-miss queries that must not start the skill. A near-miss query uses words that are close to the skill but asks for a different task. Use this model:

   ```json
   [
     { "query": "<A request that the skill must handle>", "should_trigger": true },
     {
       "query": "<A request that is close to the skill but is a different task>",
       "should_trigger": false
     },
     {
       "query": "<A request that has no link to the skill>",
       "should_trigger": false
     }
   ]
   ```

5. Write the file `skills/<skill-name>/evals/validation_queries.json` with different queries. Do not use the same queries in both files.

## Part G. Add the plugin evals

Do steps 1 to 5 for each skill. Do steps 6 to 8 one time.

1. Create the file `evals/<skill-name>-task/prompt.md`:

   ```markdown
   ---
   max_turns: 15
   allowed_tools: [Read, Glob, Grep, Skill, Agent]
   ---

   <A request that must start the skill. Write it as a user types it. Do not name the skill. Name the input files that the fixture creates.>
   ```

2. Create the file `evals/<skill-name>-task/case.yaml`:

   ```yaml
   schema_version: '1.1'
   name: <skill-name>-task
   tags: [smoke]
   context:
     scaffold_script: fixture.sh
   ```

3. Write the script `evals/<skill-name>-task/fixture.sh`. Claude Code requires a Bash script. Make the script write the input files into the workspace.
4. Create the grader `evals/<skill-name>-task/graders/criteria.md`:

   ```markdown
   ---
   type: llm
   ---

   PASS if <the condition for a correct answer>.
   FAIL if <the condition for a wrong answer>.
   ```

5. Create the grader `evals/<skill-name>-task/graders/skill-fired.md`. This grader shows if the skill started. In a run with two arms, the score does not include it. Use `criteria.md` for the score:

   ```markdown
   ---
   type: tool_used
   tool: Skill
   input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill-name>"'
   ---
   ```

6. Create the file `evals/unrelated-request/prompt.md`. Write one request that has no link to the skills, for example `Write a haiku about autumn.`
7. Create the grader `evals/unrelated-request/graders/no-skill.md`. This grader checks that no skill started:

   ```markdown
   ---
   type: tool_used
   tool: Skill
   arm: both
   min: 0
   max: 0
   ---
   ```

8. Create the file `.gitignore` with this content:

   ```txt
   evals/results/
   .workspace/
   ```
