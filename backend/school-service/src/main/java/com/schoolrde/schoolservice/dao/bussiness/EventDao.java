package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.EventEntity;

public interface EventDao{
	
    EventEntity saveEvent(EventEntity event);

    List<EventEntity> findEventBySchoolId(Integer schoolId);

    Optional<EventEntity> findEventById(Integer id);

}
