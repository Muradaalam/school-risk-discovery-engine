package com.schoolrde.schoolservice.service;

import java.util.List;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.EventDao;
import com.schoolrde.schoolservice.dto.EventRequestDto;
import com.schoolrde.schoolservice.dto.EventResponseDto;
import com.schoolrde.schoolservice.entity.EventEntity;
import com.schoolrde.schoolservice.entity.EventType;
import com.schoolrde.schoolservice.exception.CustomException;


import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

@Service
public class EventService{
	
    private static final Logger LOGGER=LoggerFactory.getLogger(EventService.class);

    private final EventDao eventDao;

    EventService(EventDao eventDao) {
        this.eventDao = eventDao;
    }
    
    @PersistenceContext
    private EntityManager entityManager;


    public List<EventResponseDto> getEventBySchoolId(Integer schoolId){

        LOGGER.info("Fetching events for schoolId : {}", schoolId);

        List<EventEntity> eventEntities = eventDao.findEventBySchoolId(schoolId);

        if(eventEntities.isEmpty()){
            LOGGER.warn("Events not found for schoolId : {}", schoolId);
            throw new CustomException("E9007");
        }

        return eventEntities.stream().map(this::convertToResponseDto)
                .collect(Collectors.toList());
    }

    public EventResponseDto getEventById(Integer id){

        EventEntity eventEntity = eventDao.findEventById(id)
                .orElseThrow(()->{
                	LOGGER.warn("Event not found with id : {}", id);
                	return new CustomException("E9007");
                });
        
        LOGGER.info("Event retrieved successfully with id : {}", id);
        return convertToResponseDto(eventEntity);
    }

    public Integer createEvent(EventRequestDto eventRequestDto){

        LOGGER.info("Creating event");

        EventEntity eventEntity = new EventEntity();
        eventEntity.setSchoolId(eventRequestDto.getSchoolId());
        EventType eventType = entityManager.getReference(EventType.class, eventRequestDto.getEventTypeId());
        eventEntity.setEventType(eventType);
        eventEntity.setDetailedDescription(eventRequestDto.getDetailedDescription());
        eventEntity.setEventDate(eventRequestDto.getEventDate());
        eventEntity.setLocation(eventRequestDto.getLocation());

        EventEntity savedEntity = eventDao.saveEvent(eventEntity);

        LOGGER.info("Event created successfully with id : {}", savedEntity.getId());

        return savedEntity.getId();
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
