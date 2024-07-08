import OpenAI from "openai";
import Client from "pg";

const translate_assistent_id = 'asst_9kQSbtwLvybo3caG7aZlryJk'
const refine_input_assistent_id = 'asst_JH7C7B3Xq0N3rIzQsQMmF8tq'
const sql_generate_assistent_id = 'asst_MYx8GhtYXLfBRDwo6kPVQxwe'
const sql_refine_assistent_id = 'asst_JmjJ89FdisqG0uuIVWG9pQg5'
const format_assistent_id = 'asst_9oWEg7QgQAGJ9fXAKbFqXNce'


const client = new OpenAI({
    apiKey: '',
});

async function callAssistent({ assistant_id, prompt }) {
    const thread = await client.beta.threads.create({
        messages: [{
            role: "user",
            content: prompt,
        },],
    });

    const run = await client.beta.threads.runs.createAndPoll(thread.id, {
        assistant_id,
    });

    const messages = await client.beta.threads.messages.list(thread.id, {
        run_id: run.id,
    });

    const message = messages.data.pop();
    const text = message.content[0].text.value;

    return { text };
}

function extractSql(text) {
    const array = text.split('```')

    return (array[1] || array[0]).trim();

}

async function sqlExecute(result) {
    const sqlQuery = result;

    const dbParams = {
        user: 'admin',
        host: 'localhost',
        database: 'postgres',
        password: '12345678',
        port: 54322,
    };

    const client = new Client.Client(dbParams);

    try {
        await client.connect();
        const res = await client.query(sqlQuery);

        console.log('*******');
        console.log('*******');
        console.log('Final result:');

        console.log(res.rows);

        await client.end();

        return res.rows;
    } catch (e) {
        console.error(`Error executing SQL query: ${e}`);
    }
}

async function main() {
    console.log('Starting ai...')
    // const prompt = "quero saber quem sao os gestores da escola bom tempo. Trazer com email e telefone."
    // const prompt = "saberia me informar se o usuario de id 55252 possui algum token de ativacao de email?"

    const prompt = "quantas escolas estao ativas no sistema com mais de um atendimento no ultimo mes?"

    console.log('translating...')
    const { text: translated } = await callAssistent({
        assistant_id: translate_assistent_id,
        prompt: `${prompt}`,
    })

    console.log('translated:', translated)
    console.log('--')


    console.log('refiniment...')
    const { text: input } = await callAssistent({
        assistant_id: refine_input_assistent_id,
        prompt: `return just the text answer: ${translated}`
    })


    console.log('sql input:', input)
    console.log('--')

    console.log('generate sql...')
    const { text: sql_result } = await callAssistent({
        assistant_id: sql_generate_assistent_id,
        prompt: `generate sql and should return only the sql result: \n\n ${input} \n\n use schema.txt to understand the database schema. \n return just the sql without any other info, the sql should be wrapped by "\`\`\`".`
    })


    console.log('sql result:', sql_result)
    console.log('--')

    const sqlRaw = extractSql(sql_result)
    console.log('raw sql: ', sqlRaw)


    const result = await sqlExecute(sqlRaw)
    console.log('execute result:', result)

    const stringData = JSON.stringify(result)
    console.log('format sql...', `answer the question if data is present: ${translated} \n for data \n ${stringData}`)


    if (stringData && stringData.length > 2000) {
        console.log('Data is too big to format. Returning raw data.')
        return stringData
    } else {
        const { text: formated_sql } = await callAssistent({
            assistant_id: format_assistent_id,
            prompt: `answer the question if data is present: ${translated} \n for data \n ${stringData}`
        })

        console.log('format result:', formated_sql)
        console.log('--')
    }
}

main();