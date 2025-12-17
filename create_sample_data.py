#!/usr/bin/env python3
"""
Create sample data for testing the Prompt Galaxy
"""

import sys
import os
sys.path.append('/home/engine/project')

from database import Database
from services import PromptService
import json

def create_sample_data():
    """Create sample prompts for testing the galaxy visualization"""
    print("Creating sample data...")
    
    # Initialize database and service
    db = Database()
    prompt_service = PromptService(db)
    
    # Sample prompts with various categories and tags
    sample_prompts = [
        {
            "title": "Code Review Request",
            "content": "Please review this {{language}} code for {{focus_area}}:\n\n```\n{{code}}\n```\n\nFocus on: {{focus_area}}",
            "category": "Development",
            "tags": ["code-review", "programming", "development", "quality"],
            "variables": [
                {
                    "name": "language",
                    "type": "select",
                    "default_value": "Python",
                    "options": ["Python", "JavaScript", "Go", "Rust"],
                },
                {
                    "name": "code",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "focus_area",
                    "type": "text",
                    "default_value": "performance",
                },
            ],
        },
        {
            "title": "Bug Report Template",
            "content": "## Bug Report: {{bug_title}}\n\n**Description:**\n{{bug_description}}\n\n**Steps to Reproduce:**\n1. {{step1}}\n2. {{step2}}\n3. {{step3}}\n\n**Expected Behavior:**\n{{expected}}\n\n**Actual Behavior:**\n{{actual}}",
            "category": "Development",
            "tags": ["bug-report", "testing", "development", "issue-tracking"],
            "variables": [
                {
                    "name": "bug_title",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "bug_description",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "step1",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "step2",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "step3",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "expected",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "actual",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Marketing Campaign Brief",
            "content": "## Marketing Campaign: {{campaign_name}}\n\n**Target Audience:**\n{{target_audience}}\n\n**Campaign Goals:**\n{{goals}}\n\n**Key Messages:**\n{{key_messages}}\n\n**Budget:** ${{budget}}\n**Timeline:** {{timeline}}\n\n**Channels:**\n- {{channel1}}\n- {{channel2}}\n- {{channel3}}",
            "category": "Marketing",
            "tags": ["marketing", "campaign", "strategy", "planning"],
            "variables": [
                {
                    "name": "campaign_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "target_audience",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "goals",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "key_messages",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "budget",
                    "type": "number",
                    "default_value": "10000",
                },
                {
                    "name": "timeline",
                    "type": "text",
                    "default_value": "Q2 2024",
                },
                {
                    "name": "channel1",
                    "type": "text",
                    "default_value": "Social Media",
                },
                {
                    "name": "channel2",
                    "type": "text",
                    "default_value": "Email",
                },
                {
                    "name": "channel3",
                    "type": "text",
                    "default_value": "Content Marketing",
                },
            ],
        },
        {
            "title": "Research Proposal Outline",
            "content": "# Research Proposal: {{research_topic}}\n\n## Abstract\n{{abstract}}\n\n## Introduction\n{{introduction}}\n\n## Literature Review\n{{literature_review}}\n\n## Research Questions\n{{research_questions}}\n\n## Methodology\n{{methodology}}\n\n## Expected Outcomes\n{{expected_outcomes}}\n\n## Timeline\n{{timeline}}\n\n## Budget\n{{budget}}",
            "category": "Research",
            "tags": ["research", "proposal", "academic", "planning"],
            "variables": [
                {
                    "name": "research_topic",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "abstract",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "introduction",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "literature_review",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "research_questions",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "methodology",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "expected_outcomes",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "timeline",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "budget",
                    "type": "text",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Code Documentation",
            "content": "# {{function_name}} Function\n\n## Purpose\n{{purpose}}\n\n## Parameters\n{{parameters}}\n\n## Returns\n{{returns}}\n\n## Example Usage\n```python\n{{example_code}}\n```\n\n## Notes\n{{notes}}",
            "category": "Documentation",
            "tags": ["documentation", "code", "development", "technical-writing"],
            "variables": [
                {
                    "name": "function_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "purpose",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "parameters",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "returns",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "example_code",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "notes",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Product Requirement Document",
            "content": "# Product Requirement: {{product_name}}\n\n## Overview\n{{overview}}\n\n## User Stories\n{{user_stories}}\n\n## Functional Requirements\n{{functional_requirements}}\n\n## Non-Functional Requirements\n{{non_functional_requirements}}\n\n## Success Metrics\n{{success_metrics}}\n\n## Timeline\n{{timeline}}",
            "category": "Planning",
            "tags": ["product", "requirements", "planning", "documentation"],
            "variables": [
                {
                    "name": "product_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "overview",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "user_stories",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "functional_requirements",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "non_functional_requirements",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "success_metrics",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "timeline",
                    "type": "text",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Performance Analysis Report",
            "content": "# Performance Analysis: {{system_name}}\n\n## Executive Summary\n{{executive_summary}}\n\n## Current Performance\n{{current_performance}}\n\n## Issues Identified\n{{issues_identified}}\n\n## Recommendations\n{{recommendations}}\n\n## Implementation Plan\n{{implementation_plan}}",
            "category": "Analysis",
            "tags": ["performance", "analysis", "reporting", "optimization"],
            "variables": [
                {
                    "name": "system_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "executive_summary",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "current_performance",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "issues_identified",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "recommendations",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "implementation_plan",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Technical Architecture Design",
            "content": "# Technical Architecture: {{project_name}}\n\n## System Overview\n{{system_overview}}\n\n## Components\n{{components}}\n\n## Data Flow\n{{data_flow}}\n\n## Technology Stack\n{{technology_stack}}\n\n## Scalability Considerations\n{{scalability}}\n\n## Security Measures\n{{security_measures}}",
            "category": "Development",
            "tags": ["architecture", "technical-design", "development", "system-design"],
            "variables": [
                {
                    "name": "project_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "system_overview",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "components",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "data_flow",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "technology_stack",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "scalability",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "security_measures",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Customer Feedback Analysis",
            "content": "# Customer Feedback Analysis: {{product_name}}\n\n## Feedback Sources\n{{feedback_sources}}\n\n## Key Themes\n{{key_themes}}\n\n## Positive Feedback\n{{positive_feedback}}\n\n## Areas for Improvement\n{{improvement_areas}}\n\n## Action Items\n{{action_items}}",
            "category": "Analysis",
            "tags": ["customer-feedback", "analysis", "product-improvement", "research"],
            "variables": [
                {
                    "name": "product_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "feedback_sources",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "key_themes",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "positive_feedback",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "improvement_areas",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "action_items",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "Content Marketing Strategy",
            "content": "# Content Marketing Strategy: {{campaign_theme}}\n\n## Content Pillars\n{{content_pillars}}\n\n## Content Calendar\n{{content_calendar}}\n\n## Distribution Channels\n{{distribution_channels}}\n\n## KPIs\n{{kpis}}\n\n## Budget Allocation\n{{budget_allocation}}",
            "category": "Marketing",
            "tags": ["content-marketing", "strategy", "marketing", "planning"],
            "variables": [
                {
                    "name": "campaign_theme",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "content_pillars",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "content_calendar",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "distribution_channels",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "kpis",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "budget_allocation",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
        {
            "title": "API Documentation Template",
            "content": "# {{api_name}} API Documentation\n\n## Overview\n{{api_overview}}\n\n## Authentication\n{{authentication}}\n\n## Endpoints\n{{endpoints}}\n\n## Request Format\n{{request_format}}\n\n## Response Format\n{{response_format}}\n\n## Examples\n{{examples}}",
            "category": "Documentation",
            "tags": ["api", "documentation", "technical-writing", "development"],
            "variables": [
                {
                    "name": "api_name",
                    "type": "text",
                    "default_value": "",
                },
                {
                    "name": "api_overview",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "authentication",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "endpoints",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "request_format",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "response_format",
                    "type": "textarea",
                    "default_value": "",
                },
                {
                    "name": "examples",
                    "type": "textarea",
                    "default_value": "",
                },
            ],
        },
    ]
    
    # Create the prompts
    created_count = 0
    for prompt_data in sample_prompts:
        try:
            # Create Variable objects from the data
            from database import Variable, VariableType
            
            variables = []
            for var_data in prompt_data["variables"]:
                var = Variable(
                    name=var_data["name"],
                    type=VariableType(var_data["type"]),
                    default_value=var_data["default_value"],
                    options=var_data.get("options")
                )
                variables.append(var)
            
            # Create the prompt
            prompt = prompt_service.create_prompt(
                title=prompt_data["title"],
                content=prompt_data["content"],
                category=prompt_data["category"],
                tags=prompt_data["tags"],
                variables=variables
            )
            
            created_count += 1
            print(f"Created: {prompt.title} ({prompt.category})")
            
        except Exception as e:
            print(f"Error creating prompt '{prompt_data['title']}': {e}")
    
    print(f"\nSuccessfully created {created_count} prompts!")
    
    # Set some favorites
    prompts = db.get_all_prompts()
    if len(prompts) >= 3:
        # Make first few prompts favorites
        for i in range(min(3, len(prompts))):
            prompt_service.toggle_favorite(prompts[i].id)
            print(f"Set as favorite: {prompts[i].title}")
    
    # Increment use count for some prompts
    if len(prompts) >= 5:
        for i in range(min(5, len(prompts))):
            for _ in range(i + 1):  # Use count from 1 to 5
                db.increment_use_count(prompts[i].id)
        print("Incremented use counts for testing")
    
    return created_count

if __name__ == "__main__":
    create_sample_data()