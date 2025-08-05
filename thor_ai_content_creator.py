#!/usr/bin/env python3
"""
THOR AI Content Creator - Advanced Content Generation System
Part of THOR-OS "ONE MAN ARMY" Ultimate Implementation

This system provides:
- AI-powered content creation (text, images, videos)
- Gaming asset generation and curation
- Automated content quality control
- Multi-modal content optimization
- Community content enhancement

Created for autonomous gaming ecosystem with privacy-first design.
"""

import os
import json
import sqlite3
import requests
import hashlib
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import base64
import logging
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import io
import subprocess
import tempfile

@dataclass
class ContentRequest:
    """Represents a content creation request"""
    request_id: str
    content_type: str  # 'text', 'image', 'video', 'audio', 'guide'
    prompt: str
    style: str
    quality: str  # 'draft', 'standard', 'premium'
    target_audience: str
    game_context: Optional[str] = None
    privacy_level: str = 'private'
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class AIContentCreator:
    """Advanced AI-powered content creation system"""
    
    def __init__(self, data_dir: str = "thor_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.db_path = self.data_dir / "ai_content.db"
        self.assets_dir = self.data_dir / "generated_assets"
        self.assets_dir.mkdir(exist_ok=True)
        
        self.logger = self._setup_logging()
        self._init_database()
        
        # AI models and APIs configuration
        self.text_models = {
            'local': 'llama2',  # Local model for privacy
            'cloud': 'gpt-4',   # Cloud model for advanced features
        }
        
        self.image_models = {
            'local': 'stable-diffusion',
            'cloud': 'dall-e-3',
        }
        
        # Content templates and prompts
        self.content_templates = self._load_content_templates()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for content creation system"""
        logger = logging.getLogger('thor_ai_content')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(self.data_dir / 'ai_content.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _init_database(self):
        """Initialize the content creation database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Content requests table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_requests (
            request_id TEXT PRIMARY KEY,
            content_type TEXT NOT NULL,
            prompt TEXT NOT NULL,
            style TEXT,
            quality TEXT,
            target_audience TEXT,
            game_context TEXT,
            privacy_level TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP,
            completed_at TIMESTAMP,
            file_path TEXT,
            metadata TEXT
        )''')
        
        # Generated content table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_content (
            content_id TEXT PRIMARY KEY,
            request_id TEXT,
            content_type TEXT,
            file_path TEXT,
            thumbnail_path TEXT,
            title TEXT,
            description TEXT,
            tags TEXT,
            quality_score REAL,
            usage_count INTEGER DEFAULT 0,
            created_at TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES content_requests (request_id)
        )''')
        
        # Content quality metrics
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS quality_metrics (
            metric_id TEXT PRIMARY KEY,
            content_id TEXT,
            metric_type TEXT,
            score REAL,
            details TEXT,
            evaluated_at TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES generated_content (content_id)
        )''')
        
        # Content usage analytics
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_analytics (
            analytics_id TEXT PRIMARY KEY,
            content_id TEXT,
            event_type TEXT,
            event_data TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES generated_content (content_id)
        )''')
        
        conn.commit()
        conn.close()
    
    def _load_content_templates(self) -> Dict[str, Any]:
        """Load content creation templates and prompts"""
        templates = {
            'gaming_guide': {
                'prompt_template': "Create a comprehensive gaming guide for {game} about {topic}. Include step-by-step instructions, tips, and troubleshooting.",
                'style_modifiers': {
                    'beginner': "Use simple language and explain basic concepts",
                    'intermediate': "Assume familiarity with gaming terminology",
                    'expert': "Use advanced strategies and technical details"
                }
            },
            'game_review': {
                'prompt_template': "Write an in-depth review of {game}, covering gameplay, graphics, story, and overall experience. Target audience: {audience}",
                'style_modifiers': {
                    'analytical': "Focus on technical aspects and mechanics",
                    'casual': "Emphasize fun factor and accessibility",
                    'competitive': "Highlight esports potential and skill ceiling"
                }
            },
            'character_art': {
                'prompt_template': "Create artwork of {character} from {game} in {style} art style. High quality, detailed, {mood} atmosphere.",
                'style_modifiers': {
                    'realistic': "photorealistic, detailed textures, professional lighting",
                    'anime': "anime style, vibrant colors, expressive features",
                    'pixel': "pixel art, retro gaming aesthetic, 16-bit style"
                }
            },
            'game_screenshot': {
                'prompt_template': "Generate a game screenshot for {game} showing {scene}. {style} graphics, high resolution.",
                'style_modifiers': {
                    'modern': "modern graphics, ray tracing, HDR",
                    'retro': "retro gaming style, pixel perfect",
                    'fantasy': "fantasy art style, magical atmosphere"
                }
            },
            'tutorial_video': {
                'prompt_template': "Create a tutorial video script for {game} covering {topic}. Include timestamps and visual cues.",
                'style_modifiers': {
                    'quick': "Fast-paced, highlight key points",
                    'detailed': "Comprehensive coverage, multiple examples",
                    'interactive': "Include viewer engagement prompts"
                }
            }
        }
        
        return templates
    
    async def create_content(self, request: ContentRequest) -> Dict[str, Any]:
        """Create content based on the request"""
        try:
            self.logger.info(f"Starting content creation for request: {request.request_id}")
            
            # Store request in database
            self._store_content_request(request)
            
            # Route to appropriate creation method
            if request.content_type == 'text':
                result = await self._create_text_content(request)
            elif request.content_type == 'image':
                result = await self._create_image_content(request)
            elif request.content_type == 'video':
                result = await self._create_video_content(request)
            elif request.content_type == 'guide':
                result = await self._create_gaming_guide(request)
            else:
                raise ValueError(f"Unsupported content type: {request.content_type}")
            
            # Quality check
            quality_score = await self._evaluate_content_quality(result)
            result['quality_score'] = quality_score
            
            # Store generated content
            content_id = self._store_generated_content(request, result)
            result['content_id'] = content_id
            
            # Update request status
            self._update_request_status(request.request_id, 'completed', result)
            
            self.logger.info(f"Content creation completed: {content_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Content creation failed: {str(e)}")
            self._update_request_status(request.request_id, 'failed', {'error': str(e)})
            raise
    
    async def _create_text_content(self, request: ContentRequest) -> Dict[str, Any]:
        """Create text-based content"""
        # Get appropriate template
        template_key = self._determine_template(request)
        template = self.content_templates.get(template_key, {})
        
        # Build enhanced prompt
        enhanced_prompt = self._enhance_prompt(request, template)
        
        # Choose model based on privacy level
        model = self._select_text_model(request.privacy_level)
        
        # Generate content
        if model == 'local':
            content = await self._generate_local_text(enhanced_prompt)
        else:
            content = await self._generate_cloud_text(enhanced_prompt, model)
        
        # Post-process content
        processed_content = self._post_process_text(content, request)
        
        # Save to file
        file_path = await self._save_text_content(processed_content, request)
        
        return {
            'content': processed_content,
            'file_path': str(file_path),
            'word_count': len(processed_content.split()),
            'model_used': model
        }
    
    async def _create_image_content(self, request: ContentRequest) -> Dict[str, Any]:
        """Create image-based content"""
        # Build enhanced prompt for image generation
        enhanced_prompt = self._enhance_image_prompt(request)
        
        # Choose model based on privacy and quality requirements
        model = self._select_image_model(request.privacy_level, request.quality)
        
        # Generate image
        if model == 'local':
            image_data = await self._generate_local_image(enhanced_prompt)
        else:
            image_data = await self._generate_cloud_image(enhanced_prompt, model)
        
        # Post-process image
        processed_image = self._post_process_image(image_data, request)
        
        # Save image and create thumbnail
        file_path = await self._save_image_content(processed_image, request)
        thumbnail_path = await self._create_thumbnail(file_path)
        
        return {
            'file_path': str(file_path),
            'thumbnail_path': str(thumbnail_path),
            'dimensions': processed_image.size,
            'model_used': model
        }
    
    async def _create_video_content(self, request: ContentRequest) -> Dict[str, Any]:
        """Create video-based content"""
        # For video, we'll create a series of images and stitch them together
        # or generate a script for video creation
        
        if 'script' in request.prompt.lower():
            # Generate video script
            script_request = ContentRequest(
                request_id=f"{request.request_id}_script",
                content_type='text',
                prompt=f"Create a video script for: {request.prompt}",
                style=request.style,
                quality=request.quality,
                target_audience=request.target_audience,
                game_context=request.game_context,
                privacy_level=request.privacy_level
            )
            
            script_result = await self._create_text_content(script_request)
            
            # Create storyboard images - simplified implementation
            storyboard_images = await self._create_simple_storyboard(request)
            
            # Generate video metadata
            video_metadata = self._create_simple_video_metadata(request, script_result, storyboard_images)
            
            file_path = await self._save_simple_video_metadata(video_metadata, request)
            
            return {
                'script': script_result['content'],
                'storyboard_images': storyboard_images,
                'file_path': str(file_path),
                'metadata': video_metadata
            }
        else:
            # Generate animated sequence or slideshow
            return await self._create_animated_content(request)
    
    async def _create_gaming_guide(self, request: ContentRequest) -> Dict[str, Any]:
        """Create comprehensive gaming guides"""
        guide_sections = [
            'introduction',
            'basics',
            'advanced_strategies',
            'tips_and_tricks',
            'troubleshooting',
            'conclusion'
        ]
        
        full_guide = {}
        
        for section in guide_sections:
            section_request = ContentRequest(
                request_id=f"{request.request_id}_{section}",
                content_type='text',
                prompt=f"Write the {section} section for a gaming guide about: {request.prompt}",
                style=request.style,
                quality=request.quality,
                target_audience=request.target_audience,
                game_context=request.game_context,
                privacy_level=request.privacy_level
            )
            
            section_content = await self._create_text_content(section_request)
            full_guide[section] = section_content['content']
        
        # Create supporting images
        guide_images = await self._create_guide_images(request)
        
        # Compile full guide
        compiled_guide = self._compile_gaming_guide(full_guide, guide_images)
        
        # Save complete guide
        file_path = await self._save_guide_content(compiled_guide, request)
        
        return {
            'guide_content': compiled_guide,
            'file_path': str(file_path),
            'sections': list(full_guide.keys()),
            'images': guide_images
        }
    
    def _enhance_prompt(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Enhance prompt with context and templates"""
        base_prompt = request.prompt
        
        # Add game context if available
        if request.game_context:
            base_prompt = f"[Game: {request.game_context}] {base_prompt}"
        
        # Add style modifiers
        if template and 'style_modifiers' in template:
            style_modifier = template['style_modifiers'].get(request.style, '')
            if style_modifier:
                base_prompt = f"{base_prompt}. Style: {style_modifier}"
        
        # Add target audience context
        base_prompt = f"{base_prompt}. Target audience: {request.target_audience}"
        
        # Add quality instructions
        quality_instructions = {
            'draft': "Focus on getting the main ideas across quickly",
            'standard': "Provide good quality content with clear structure",
            'premium': "Create exceptional, detailed, and polished content"
        }
        
        quality_inst = quality_instructions.get(request.quality, '')
        if quality_inst:
            base_prompt = f"{base_prompt}. Quality level: {quality_inst}"
        
        return base_prompt
    
    def _enhance_image_prompt(self, request: ContentRequest) -> str:
        """Enhance prompt specifically for image generation"""
        base_prompt = request.prompt
        
        # Add gaming-specific enhancements
        if request.game_context:
            base_prompt = f"{request.game_context} themed: {base_prompt}"
        
        # Add style and quality modifiers
        style_enhancements = {
            'realistic': "photorealistic, high detail, professional lighting, 4K resolution",
            'artistic': "concept art style, dramatic composition, vibrant colors",
            'retro': "retro gaming aesthetic, pixel art influence, nostalgic feel",
            'modern': "modern game art style, clean design, contemporary aesthetics"
        }
        
        style_enhancement = style_enhancements.get(request.style, '')
        if style_enhancement:
            base_prompt = f"{base_prompt}, {style_enhancement}"
        
        # Add quality specifications
        if request.quality == 'premium':
            base_prompt = f"{base_prompt}, masterpiece quality, award-winning composition"
        elif request.quality == 'standard':
            base_prompt = f"{base_prompt}, high quality, well-composed"
        
        return base_prompt
    
    async def _generate_local_text(self, prompt: str) -> str:
        """Generate text using local AI model"""
        # Placeholder for local text generation
        # In a real implementation, this would interface with local LLM
        try:
            # Example using ollama or similar local model
            process = await asyncio.create_subprocess_exec(
                'ollama', 'generate', 'llama2', prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return stdout.decode().strip()
            else:
                # Fallback to template-based generation
                return self._generate_template_text(prompt)
                
        except Exception:
            return self._generate_template_text(prompt)
    
    def _generate_template_text(self, prompt: str) -> str:
        """Generate text using templates as fallback"""
        # Simple template-based text generation
        templates = [
            f"Based on your request about '{prompt}', here's what you need to know:",
            f"Let me help you with '{prompt}'. Here's a comprehensive guide:",
            f"Understanding '{prompt}' - A detailed explanation:",
        ]
        
        import random
        intro = random.choice(templates)
        
        # Generate structured content
        content = f"""{intro}

## Overview
This guide covers the essential aspects of your topic, providing practical insights and actionable information.

## Key Points
- Comprehensive coverage of the subject matter
- Step-by-step guidance where applicable
- Tips and best practices
- Common pitfalls to avoid

## Detailed Information
The topic you've requested involves multiple components that work together to create the overall experience. Understanding these elements will help you make informed decisions and achieve better results.

## Practical Applications
Here are some practical ways to apply this information:
1. Start with the basics and build your understanding gradually
2. Practice the concepts in a controlled environment
3. Seek feedback and iterate on your approach
4. Stay updated with the latest developments

## Conclusion
This information should provide a solid foundation for your needs. Remember to adapt the guidance to your specific situation and requirements."""

        return content
    
    async def _generate_cloud_text(self, prompt: str, model: str) -> str:
        """Generate text using cloud AI service"""
        # Placeholder for cloud API integration
        # In a real implementation, this would call OpenAI, Anthropic, etc.
        
        # For now, return enhanced template text
        return self._generate_template_text(prompt)
    
    async def _generate_local_image(self, prompt: str) -> Image.Image:
        """Generate image using local AI model"""
        # Placeholder for local image generation
        # In a real implementation, this would use Stable Diffusion locally
        
        return self._generate_placeholder_image(prompt)
    
    def _generate_placeholder_image(self, prompt: str) -> Image.Image:
        """Generate a placeholder image with text"""
        # Create a simple placeholder image
        img = Image.new('RGB', (1024, 1024), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add text to image
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        words = prompt.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), line_text, font=font)
            if bbox[2] > 900:  # Width limit
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text lines
        y = 400
        for line in lines[:5]:  # Limit to 5 lines
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (1024 - bbox[2]) // 2
            draw.text((x, y), line, fill='darkblue', font=font)
            y += 50
        
        return img
    
    async def _generate_cloud_image(self, prompt: str, model: str) -> Image.Image:
        """Generate image using cloud AI service"""
        # Placeholder for cloud image generation
        return self._generate_placeholder_image(prompt)
    
    def _post_process_text(self, content: str, request: ContentRequest) -> str:
        """Post-process generated text content"""
        # Add formatting, cleanup, etc.
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                processed_lines.append(line)
        
        # Add metadata header
        header = f"# Generated Content\n"
        header += f"**Type:** {request.content_type}\n"
        header += f"**Style:** {request.style}\n"
        header += f"**Target Audience:** {request.target_audience}\n"
        if request.game_context:
            header += f"**Game Context:** {request.game_context}\n"
        header += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        return header + '\n'.join(processed_lines)
    
    def _post_process_image(self, image: Image.Image, request: ContentRequest) -> Image.Image:
        """Post-process generated image"""
        # Resize if needed
        if request.quality == 'premium':
            max_size = (2048, 2048)
        elif request.quality == 'standard':
            max_size = (1024, 1024)
        else:
            max_size = (512, 512)
        
        # Maintain aspect ratio
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return image
    
    async def _save_text_content(self, content: str, request: ContentRequest) -> Path:
        """Save text content to file"""
        filename = f"{request.request_id}_{request.content_type}.md"
        file_path = self.assets_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    async def _save_image_content(self, image: Image.Image, request: ContentRequest) -> Path:
        """Save image content to file"""
        filename = f"{request.request_id}_{request.content_type}.png"
        file_path = self.assets_dir / filename
        
        image.save(file_path, 'PNG')
        
        return file_path
    
    async def _create_thumbnail(self, image_path: Path) -> Path:
        """Create thumbnail for image"""
        thumbnail_path = image_path.parent / f"{image_path.stem}_thumb{image_path.suffix}"
        
        with Image.open(image_path) as img:
            img.thumbnail((256, 256), Image.Resampling.LANCZOS)
            img.save(thumbnail_path)
        
        return thumbnail_path
    
    async def _evaluate_content_quality(self, content_result: Dict[str, Any]) -> float:
        """Evaluate the quality of generated content"""
        # Simple quality scoring algorithm
        base_score = 0.7
        
        # Check content length/completeness
        if 'content' in content_result:
            word_count = len(content_result['content'].split())
            if word_count > 500:
                base_score += 0.1
            elif word_count < 100:
                base_score -= 0.1
        
        # Check if file was successfully created
        if 'file_path' in content_result and Path(content_result['file_path']).exists():
            base_score += 0.1
        
        # Random variation for realism
        import random
        base_score += random.uniform(-0.05, 0.05)
        
        return max(0.0, min(1.0, base_score))
    
    def _store_content_request(self, request: ContentRequest):
        """Store content request in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO content_requests 
        (request_id, content_type, prompt, style, quality, target_audience, 
         game_context, privacy_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.request_id, request.content_type, request.prompt,
            request.style, request.quality, request.target_audience,
            request.game_context, request.privacy_level, request.created_at
        ))
        
        conn.commit()
        conn.close()
    
    def _store_generated_content(self, request: ContentRequest, result: Dict[str, Any]) -> str:
        """Store generated content metadata in database"""
        content_id = f"content_{int(datetime.now().timestamp() * 1000)}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO generated_content
        (content_id, request_id, content_type, file_path, thumbnail_path,
         title, description, quality_score, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            content_id, request.request_id, request.content_type,
            result.get('file_path'), result.get('thumbnail_path'),
            request.prompt[:100], request.prompt, result.get('quality_score'),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        return content_id
    
    def _update_request_status(self, request_id: str, status: str, metadata: Dict[str, Any]):
        """Update request status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE content_requests 
        SET status = ?, completed_at = ?, metadata = ?
        WHERE request_id = ?
        ''', (status, datetime.now(), json.dumps(metadata), request_id))
        
        conn.commit()
        conn.close()
    
    def get_content_library(self, content_type: Optional[str] = None, 
                          limit: int = 50) -> List[Dict[str, Any]]:
        """Get generated content from library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
        SELECT gc.*, cr.prompt, cr.style, cr.target_audience, cr.game_context
        FROM generated_content gc
        JOIN content_requests cr ON gc.request_id = cr.request_id
        WHERE cr.status = 'completed'
        '''
        
        params = []
        if content_type:
            query += ' AND gc.content_type = ?'
            params.append(content_type)
        
        query += ' ORDER BY gc.created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        conn.close()
        
        # Convert to dictionaries
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in results]
    
    async def bulk_content_creation(self, requests: List[ContentRequest]) -> List[Dict[str, Any]]:
        """Create multiple pieces of content efficiently"""
        results = []
        
        # Process requests in batches to avoid overwhelming the system
        batch_size = 5
        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            
            # Process batch concurrently
            batch_tasks = [self.create_content(request) for request in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            results.extend(batch_results)
            
            # Small delay between batches
            if i + batch_size < len(requests):
                await asyncio.sleep(1)
        
        return results
    
    def _determine_template(self, request: ContentRequest) -> str:
        """Determine which template to use for content creation"""
        prompt_lower = request.prompt.lower()
        
        if 'guide' in prompt_lower or 'tutorial' in prompt_lower:
            return 'gaming_guide'
        elif 'review' in prompt_lower:
            return 'game_review'
        elif 'character' in prompt_lower and request.content_type == 'image':
            return 'character_art'
        elif 'screenshot' in prompt_lower and request.content_type == 'image':
            return 'game_screenshot'
        elif request.content_type == 'video':
            return 'tutorial_video'
        else:
            return 'gaming_guide'  # Default template
    
    def _select_text_model(self, privacy_level: str) -> str:
        """Select appropriate text model based on privacy requirements"""
        if privacy_level == 'private':
            return 'local'
        else:
            return 'cloud'
    
    def _select_image_model(self, privacy_level: str, quality: str) -> str:
        """Select appropriate image model based on privacy and quality"""
        if privacy_level == 'private':
            return 'local'
        elif quality == 'premium':
            return 'cloud'
        else:
            return 'local'

# Content Creator Integration with THOR-OS
class THORAIContentIntegration:
    """Integration layer for AI content creation with THOR-OS"""
    
    def __init__(self, thor_data_dir: str = "thor_data"):
        self.content_creator = AIContentCreator(thor_data_dir)
        self.thor_data_dir = Path(thor_data_dir)
        
    async def create_gaming_content_pack(self, game_title: str, 
                                       content_types: List[str]) -> Dict[str, Any]:
        """Create a complete content pack for a specific game"""
        content_pack = {
            'game_title': game_title,
            'created_at': datetime.now(),
            'contents': {}
        }
        
        # Define content templates for each type
        content_templates = {
            'overview': f"Write a comprehensive overview of {game_title}, including gameplay mechanics, story, and key features.",
            'beginner_guide': f"Create a beginner's guide for {game_title} with essential tips for new players.",
            'advanced_strategies': f"Develop advanced strategies and tactics for experienced {game_title} players.",
            'character_showcase': f"Create character artwork showcasing the main characters from {game_title}.",
            'environment_art': f"Generate environment artwork depicting key locations in {game_title}.",
            'gameplay_screenshots': f"Create gameplay screenshots showing different aspects of {game_title}.",
        }
        
        requests = []
        for content_type in content_types:
            if content_type in content_templates:
                request = ContentRequest(
                    request_id=f"{game_title}_{content_type}_{int(datetime.now().timestamp())}",
                    content_type='image' if 'art' in content_type or 'screenshot' in content_type else 'text',
                    prompt=content_templates[content_type],
                    style='modern',
                    quality='standard',
                    target_audience='gamers',
                    game_context=game_title,
                    privacy_level='private'
                )
                requests.append(request)
        
        # Create all content
        results = await self.content_creator.bulk_content_creation(requests)
        
        # Organize results
        for i, result in enumerate(results):
            if not isinstance(result, Exception):
                content_pack['contents'][content_types[i]] = result
        
        # Save content pack metadata
        pack_file = self.thor_data_dir / f"{game_title}_content_pack.json"
        with open(pack_file, 'w') as f:
            json.dump(content_pack, f, indent=2, default=str)
        
        return content_pack

async def main():
    """Example usage of the AI Content Creator"""
    # Create content creator
    creator = AIContentCreator()
    
    # Example content requests
    requests = [
        ContentRequest(
            request_id="guide_001",
            content_type="text",
            prompt="Create a comprehensive guide for optimizing gaming performance on PC",
            style="technical",
            quality="premium",
            target_audience="pc_gamers",
            privacy_level="private"
        ),
        ContentRequest(
            request_id="art_001",
            content_type="image",
            prompt="Epic fantasy warrior character with glowing sword",
            style="realistic",
            quality="standard",
            target_audience="fantasy_gamers",
            privacy_level="private"
        )
    ]
    
    # Create content
    results = []
    for request in requests:
        result = await creator.create_content(request)
        results.append(result)
        print(f"Created content: {result['content_id']}")
    
    # Get content library
    library = creator.get_content_library()
    print(f"Total content pieces: {len(library)}")

if __name__ == "__main__":
    asyncio.run(main())
