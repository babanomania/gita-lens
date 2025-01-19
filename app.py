# Import necessary libraries
from typing import TypedDict, Annotated, Sequence
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.schema.output_parser import StrOutputParser
from langgraph.graph import Graph, END
import chainlit as cl
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize LLM
logger.info("Initializing LLM...")
llm = OllamaLLM(model="llama3.2")
output_parser = StrOutputParser()

# Define state types
class StoryState(TypedDict):
    theme: str
    core_story: str | None
    characters: str | None
    narrative: str | None
    refined_story: str | None
    messages: list[str]

# Define processing functions
async def generate_core_story(state: StoryState) -> StoryState:
    logger.info("Step 1/4: Starting core story generation...")
    story_architect_prompt = PromptTemplate(
        input_variables=["theme"],
        template=(
            "You are a philosopher deeply versed in the Bhagavad Gita. Based on the theme '{theme}', "
            "create a contemporary life problem or dilemma that many people face today. "
            "The problem should be relatable, emotionally resonant, and complex enough to warrant "
            "spiritual guidance. Frame it in 2-3 sentences, focusing on the internal struggle "
            "and ethical complexity, similar to Arjuna's dilemma in the Bhagavad Gita."
        ),
    )
    chain = story_architect_prompt | llm | output_parser
    
    core_story = await chain.ainvoke({"theme": state["theme"]})
    logger.info("Step 1/4: Core story generation completed")
    
    return {"theme": state["theme"], "core_story": core_story, "characters": None, 
            "narrative": None, "refined_story": None, "messages": state["messages"]}

async def create_characters(state: StoryState) -> StoryState:
    logger.info("Step 2/4: Starting character creation...")
    character_creator_prompt = PromptTemplate(
        input_variables=["core_story"],
        template=(
            "For this modern dilemma: {core_story}\n"
            "Create 2-3 main characters, including:\n"
            "1. A protagonist facing the central conflict, similar to Arjuna's position of uncertainty\n"
            "2. A wise mentor figure (like Krishna) who can offer guidance through Bhagavad Gita's teachings\n"
            "3. (Optional) A supporting character affected by the protagonist's decisions\n\n"
            "For each character, describe their internal struggles, beliefs, and how they relate to the core conflict. "
            "Make them realistic and relatable to modern readers while embodying timeless spiritual qualities."
        ),
    )
    chain = character_creator_prompt | llm | output_parser
    
    characters = await chain.ainvoke({"core_story": state["core_story"]})
    logger.info("Step 2/4: Character creation completed")
    
    return {**state, "characters": characters}

async def weave_plot(state: StoryState) -> StoryState:
    logger.info("Step 3/4: Starting plot development...")
    plot_weaver_prompt = PromptTemplate(
        input_variables=["core_story", "characters"],
        template=(
            "Using this modern dilemma: {core_story}\n"
            "And these characters: {characters}\n\n"
            "Create a narrative in 4 distinct parts:\n"
            "1. Establish the protagonist's situation and the mounting tension of their problem\n"
            "2. Show their initial attempts to solve it and why these attempts fall short\n"
            "3. Introduce the mentor's guidance, specifically drawing from relevant Bhagavad Gita teachings such as:\n"
            "   - Karma Yoga (selfless action)\n"
            "   - Dharma (duty and righteousness)\n"
            "   - The nature of the self and attachment\n"
            "   - The importance of right action over results\n"
            "4. Demonstrate how applying these teachings transforms the protagonist's understanding "
            "and leads to a resolution\n\n"
            "Keep the narrative focused on the internal transformation while making the external "
            "situation relatable to modern readers."
        ),
    )
    chain = plot_weaver_prompt | llm | output_parser
    
    narrative = await chain.ainvoke({
        "core_story": state["core_story"],
        "characters": state["characters"]
    })
    logger.info("Step 3/4: Plot development completed")
    
    return {**state, "narrative": narrative}

async def refine_story(state: StoryState) -> StoryState:
    logger.info("Step 4/4: Starting final story refinement...")
    stylist_prompt = PromptTemplate(
        input_variables=["narrative"],
        template=(
            "Take this narrative: {narrative}\n\n"
            "Enhance it into a polished story that:\n"
            "1. Clearly presents the modern problem and makes readers empathize with the protagonist's struggle\n"
            "2. Weaves in Bhagavad Gita's teachings naturally through dialogue and reflection\n"
            "3. Shows a clear transformation in the protagonist's understanding\n"
            "4. Connects the resolution to universal principles from the Gita\n\n"
            "Add meaningful dialogues between the mentor and protagonist that echo Krishna-Arjuna conversations, "
            "but in contemporary language. Include specific verses or concepts from the Bhagavad Gita where relevant, "
            "explaining them in accessible terms.\n\n"
            "The final story should be engaging and profound, under 2000 words, with clear paragraphs "
            "and a balance of action, dialogue, and reflection."
        ),
    )
    chain = stylist_prompt | llm | output_parser
    
    refined_story = await chain.ainvoke({"narrative": state["narrative"]})
    logger.info("Step 4/4: Final story refinement completed")
    
    return {**state, "refined_story": refined_story}

async def create_story_workflow(theme: str) -> str:
    """
    Orchestrate the story creation process.
    """
    try:
        logger.info(f"Starting story generation workflow for theme: {theme}")
        
        state = {"theme": theme, "messages": []}
        
        # Generate core story concept
        state = await generate_core_story(state)
        
        # Create characters
        state = await create_characters(state)
        
        # Develop the plot
        state = await weave_plot(state)
        
        # Refine and polish the story
        state = await refine_story(state)
        
        logger.info("Story generation workflow completed successfully")
        return state["refined_story"]
        
    except Exception as e:
        logger.error(f"Error in story generation workflow: {str(e)}", exc_info=True)
        raise

# Step 1: Agent to Generate Themes
theme_generator_prompt = PromptTemplate(
    input_variables=[],
    template=(
        "Generate exactly 5 moral themes from the Bhagavad Gita's teachings. "
        "Each theme must be on a new line and follow this exact format without any additional text:\n\n"
        "'Theme Name (Sanskrit Term) - Brief one-sentence description'\n\n"
        "Required format examples:\n"
        "Duty (Karma Yoga) - The struggle of fulfilling one's responsibilities without attachment\n"
        "Renunciation (Sanyasa Yoga) - A journey of letting go of worldly desires\n"
        "Compassion (Karuna) - Acts of selfless love and kindness\n\n"
        "Rules:\n"
        "1. Each line must contain exactly one theme\n"
        "2. Include the Sanskrit term in parentheses\n"
        "3. Provide a clear, concise description after the hyphen\n"
        "4. Do not add any additional text, numbers, or explanations\n"
        "5. Do not use asterisks or other formatting\n\n"
        "Generate 5 new themes now:"
    ),
)
# Create runnable chain
theme_generator_chain = theme_generator_prompt | llm | output_parser

def get_themes():
    """
    Generate themes dynamically using the theme generator agent.
    """
    try:
        logger.info("Starting theme generation...")
        start_time = time.time()
        
        response = theme_generator_chain.invoke({})
        # logger.info(f"Raw theme response: {response}")
        
        themes = []
        for line in response.split('\n'):
            line = line.strip()
            if line and ' - ' in line and '(' in line and ')' in line:
                line = line.replace('*', '').split('.')[0].strip()
                themes.append(line)
        
        #logger.info(f"Processed themes: {themes}")
        logger.info(f"Theme generation took {time.time() - start_time:.2f} seconds")
        return themes
    except Exception as e:
        logger.error(f"Error in theme generation: {str(e)}", exc_info=True)
        raise

# Step 3: Chainlit UI with Dynamic Theme Generation
@cl.on_chat_start
async def start():
    """
    Initialize the chat session and display theme options.
    """
    try:
        # Show loading message while generating themes
        await cl.Message(content="🎨 Generating theme options... Please wait.").send()
        
        themes = get_themes()
        logger.info("Themes generated successfully")
        
        # Create theme selection actions with proper payload
        actions = [
            cl.Action(
                name="select_theme",
                payload={"theme": theme},  # payload is required
                label=theme,
                description=f"Generate a story about {theme}",
                timeout=300
            )
            for theme in themes
        ]
        
        # Remove the loading message and show themes
        await cl.Message(
            content="🌟 Choose a theme for your story or type your own:",
            actions=actions
        ).send()
        
    except Exception as e:
        logger.error(f"Error in chat start: {str(e)}", exc_info=True)
        await cl.Message(content="⚠️ An error occurred while loading themes. Please refresh the page.").send()

@cl.action_callback("select_theme")
async def on_action(action):
    """
    Handle theme selection action.
    """
    try:
        theme = action.payload["theme"]
        logger.info(f"Theme selected: {theme}")
        
        # Increase client timeout to prevent "Could not reach the server" message
        await cl.Message(content="🌟 Creating a story inspired by your theme... This may take a few minutes.").send()
        
        # Set session timeout to 10 minutes
        cl.user_session.timeout = 600
        
        story = await create_story_workflow(theme=theme)
        logger.info("Story generation completed")
            
        # Send only the final story with markdown formatting
        await cl.Message(content=f"📖 Your Story: \n\n## {theme}\n\n{story}").send()
        
    except Exception as e:
        logger.error(f"Error in action handler: {str(e)}", exc_info=True)
        await cl.Message(content="⚠️ An error occurred while generating the story. Please try again.").send()

@cl.on_message
async def main(message):
    """
    Generate a story when the user inputs a theme manually.
    """
    try:
        user_theme = message.content.strip()
        logger.info(f"Received manual theme input: {user_theme}")
        
        # Increase client timeout to prevent "Could not reach the server" message
        await cl.Message(content="🌟 Creating a story inspired by your theme... This may take a few minutes.", timeout=600).send()
        
        # Set session timeout to 10 minutes
        cl.user_session.timeout = 600
        
        story = await create_story_workflow(theme=user_theme)
        logger.info("Story generation completed")
            
        # Send only the final story with markdown formatting
        await cl.Message(content=f"# 📖 Your Story\n\n{story}", timeout=600).send()
        
    except Exception as e:
        logger.error(f"Error in message handler: {str(e)}", exc_info=True)
        await cl.Message(content="⚠️ An error occurred while generating the story. Please try again.").send()
