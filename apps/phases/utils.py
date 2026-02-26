def generate_prompt(phase, form_data):
    """
    Generates a prompt by interleaving PromptChunks and PhaseFields based on order.
    Logic: Chunk[i] + Field[i] + Chunk[i+1] + ...
    """
    chunks = list(phase.prompt_chunks.all().order_by('order'))
    fields = list(phase.fields.all().order_by('order'))
    
    prompt_parts = []
    max_len = max(len(chunks), len(fields))
    
    for i in range(max_len):
        # Determine if we should include the chunk
        include_chunk = True
        chunk_content = ""
        
        if i < len(chunks):
            chunk = chunks[i]
            chunk_content = chunk.content
            
            # Check optionality logic
            # If chunk is optional, and the corresponding field (i) is empty or missing, skip chunk.
            if chunk.is_optional:
                # Check corresponding field existence
                if i < len(fields):
                    field_name = fields[i].field_name
                    if not form_data.get(field_name):
                        include_chunk = False
                else:
                    # Optional chunk with no following field? Maybe include? 
                    # Or maybe it depends on previous field?
                    # Default to including if no field condition to check, or excluding?
                    # Let's assume include if no field to check against.
                    pass
        
        if i < len(chunks) and include_chunk:
            prompt_parts.append(chunk_content)
            
        if i < len(fields):
            field = fields[i]
            value = form_data.get(field.field_name, "")
            if value:
                prompt_parts.append(str(value))
                
    return "".join(prompt_parts)
