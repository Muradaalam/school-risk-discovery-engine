package com.schoolrde.schoolservice.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.EventDao;
import com.schoolrde.schoolservice.dao.bussiness.SchoolDao;
import com.schoolrde.schoolservice.dto.EventResponseDto;
import com.schoolrde.schoolservice.dto.SchoolResponseDto;
import com.schoolrde.schoolservice.entity.EventEntity;
import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.exception.CustomException;

@Service
public class EventService{
	
    private static final Logger LOGGER=LoggerFactory.getLogger(EventService.class);
    


    @Autowired
    private EventDao eventDao;

    public EventResponseDto getEventById(Integer id){

        EventEntity eventEntity = eventDao.findById(id)
                .orElseThrow(()->{
                	LOGGER.warn("Event not found with id : {}", id);
                	return new CustomException("E9007");
                });
        LOGGER.info("Event retrieved successfully with id : {}", id);
        return convertToResponseDto(eventEntity);
    }


    private EventResponseDto convertToResponseDto(EventEntity eventEntity){
        LOGGER.info("Creating eventResponseDto...");
        
        EventResponseDto eventResponseDto = new EventResponseDto();

        eventResponseDto.setId(eventEntity.getId());
        eventResponseDto.setSchoolId(eventEntity.getSchoolId());
        eventResponseDto.setEventType(eventEntity.getEventType().getEventType());
        eventResponseDto.setDetailedDescription(eventEntity.getDetailedDescription());
        eventResponseDto.setEventDate(eventEntity.getEventDate());
        eventResponseDto.setLocation(eventEntity.getLocation());

        return eventResponseDto;

    }
}